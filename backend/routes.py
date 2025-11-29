from fastapi import APIRouter, Depends, HTTPException, Query, Header, Body, Request
from fastapi.responses import FileResponse, RedirectResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
import urllib.parse

import services
import models
import vcard_utils
from database import get_db
from security import create_access_token, decode_token, verify_password, hash_password

router = APIRouter(prefix="/api", tags=["digital-cards"])


# ========== Dependency: Extract user from token ==========

async def get_current_user(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Extract current user from JWT token.
    
    Supports two authentication methods:
    1. Header: Authorization: Bearer <token>
    2. Query parameter: ?token=<token>
    """
    # Extract token from Authorization header or query parameter
    extracted_token = None
    
    if authorization:
        # Extract Bearer token from Authorization header
        if authorization.startswith("Bearer "):
            extracted_token = authorization[7:]  # Remove "Bearer " prefix
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization header")
    elif token:
        # Use token from query parameter
        extracted_token = token
    else:
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        payload = decode_token(extracted_token)
        user_id = uuid.UUID(payload.get("sub"))
        company_id = payload.get("company_id")
        if company_id:
            company_id = uuid.UUID(company_id)
        role = payload.get("role", "employee")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    user = await services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {"user_id": user_id, "company_id": company_id, "role": role, "user": user}


# ========== Public Routes ==========

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/auth/signup", response_model=models.TokenResponse)
async def signup(user_data: models.UserCreate, db: AsyncSession = Depends(get_db)):
    """Sign up a new user (company admin)."""
    existing_user = await services.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create company for new user
    company_data = models.CompanyCreate(
        name=f"{user_data.full_name}'s Company",
        domain=None,
    )
    company = await services.create_company(db, company_data)
    
    # Create admin user
    user = await services.create_user(db, user_data, company_id=company.id)
    
    # Generate token
    access_token = create_access_token(
        user_id=user.id,
        company_id=company.id,
        role=user.role,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "company_id": company.id,
        "role": user.role,
    }


@router.post("/auth/change-password")
async def change_password(
    password_data: dict = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change user password (authenticated users only)."""
    user_id = current_user.get("user_id")
    current_password = password_data.get("current_password")
    new_password = password_data.get("new_password")
    
    if not user_id or not current_password or not new_password:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    user = await services.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    # Update password
    user.password_hash = hash_password(new_password)
    db.add(user)
    await db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/auth/reset-password-request")
async def reset_password_request(
    reset_data: dict = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """Request password reset via email (placeholder implementation)."""
    email = reset_data.get("email")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    user = await services.get_user_by_email(db, email)
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If an account with this email exists, a reset link has been sent"}
    
    # TODO: In production, send email with reset token
    # For now, just return success message
    # In a real app, you would:
    # 1. Generate a reset token
    # 2. Store it in database with expiration
    # 3. Send email with reset link containing the token
    
    return {"message": "Password reset link sent to email"}


@router.post("/auth/login", response_model=models.TokenResponse)
async def login(credentials: models.UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user."""
    user = await services.get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        user_id=user.id,
        company_id=user.company_id,
        role=user.role,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "company_id": user.company_id,
        "role": user.role,
    }


# ========== Public Card View ==========

@router.get("/card/{company_slug}/{employee_slug}", response_model=models.BusinessCardResponse)
async def get_public_card(
    company_slug: str,
    employee_slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Get public digital card view (no auth required)."""
    employee = await services.get_employee_by_slug(db, company_slug, employee_slug)
    if not employee:
        raise HTTPException(status_code=404, detail="Card not found")
    
    card = await services.get_card_by_employee(db, employee.id)
    
    return models.BusinessCardResponse(
        employee_id=employee.id,
        employee_name=employee.full_name,
        company_name=employee.company.name,
        company_id=employee.company.id,
        job_title=employee.job_title,
        email=employee.email,
        phone=employee.phone,
        whatsapp=employee.whatsapp,
        bio=employee.bio,
        photo_url=employee.photo_url,
        social_links=employee.social_links,
        qr_code=card.qr_code if card else None,
        vcard_url=card.vcard_url if card else None,
        company_logo=employee.company.logo_url,
        company_brand_color=employee.company.brand_color,
    )


# ========== Company Admin Routes ==========

@router.post("/company", response_model=models.CompanyResponse)
async def create_company_endpoint(
    company_data: models.CompanyCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new company (admin only)."""
    if current_user["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    company = await services.create_company(db, company_data)
    return company


@router.get("/company/{company_id}", response_model=models.CompanyResponse)
async def get_company_endpoint(
    company_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get company details."""
    if current_user["company_id"] != company_id and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    company = await services.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company


@router.put("/company/{company_id}", response_model=models.CompanyResponse)
async def update_company_endpoint(
    company_id: uuid.UUID,
    company_update: models.CompanyUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update company details (name, domain, logo, brand color)."""
    if current_user["company_id"] != company_id and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    company = await services.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Validate brand_color if provided
    if company_update.brand_color:
        color = company_update.brand_color
        if not isinstance(color, str) or (not color.startswith("#") or len(color) not in (7, 4)):
            raise HTTPException(status_code=400, detail="Invalid color format. Use hex format: #RGB or #RRGGBB")
    
    # Update company
    updated_data = company_update.dict(exclude_unset=True)
    company = await services.update_company(db, company_id, updated_data)
    
    return company


# ========== Employee Routes ==========

@router.post("/company/{company_id}/employees", response_model=models.EmployeeResponse)
async def create_employee_endpoint(
    company_id: uuid.UUID,
    employee_data: models.EmployeeCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new employee for a company."""
    if current_user["company_id"] != company_id and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    employee = await services.create_employee(db, company_id, employee_data)
    # Convert to dict and add company slug
    emp_data = models.EmployeeResponse.from_orm(employee).dict()
    if hasattr(employee, 'company') and employee.company:
        emp_data['company_slug'] = employee.company.slug
    return emp_data


@router.get("/company/{company_id}/employees", response_model=List[models.EmployeeResponse])
async def list_employees_endpoint(
    company_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List employees for a company."""
    if current_user["company_id"] != company_id and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    employees = await services.list_employees(db, company_id, skip, limit)
    # Add company slug to each employee
    result = []
    for employee in employees:
        emp_data = models.EmployeeResponse.from_orm(employee).dict()
        if hasattr(employee, 'company') and employee.company:
            emp_data['company_slug'] = employee.company.slug
        result.append(emp_data)
    return result


@router.get("/employees/{employee_id}", response_model=models.EmployeeResponse)
async def get_employee_endpoint(
    employee_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get employee details."""
    employee = await services.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Multi-tenant check
    if employee.company_id != current_user["company_id"] and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Convert to dict and add company slug
    emp_data = models.EmployeeResponse.from_orm(employee).dict()
    if hasattr(employee, 'company') and employee.company:
        emp_data['company_slug'] = employee.company.slug
    return emp_data


@router.put("/employees/{employee_id}", response_model=models.EmployeeResponse)
async def update_employee_endpoint(
    employee_id: uuid.UUID,
    employee_data: models.EmployeeUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update employee profile."""
    employee = await services.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Multi-tenant check: employee can only update their own, admin can update all in their company
    if current_user["role"] == "employee" and current_user["user"].id != employee_id:
        raise HTTPException(status_code=403, detail="Can only update your own profile")
    
    if employee.company_id != current_user["company_id"] and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    updated_employee = await services.update_employee(db, employee_id, employee_data)
    # Convert to dict and add company slug
    emp_data = models.EmployeeResponse.from_orm(updated_employee).dict()
    if hasattr(updated_employee, 'company') and updated_employee.company:
        emp_data['company_slug'] = updated_employee.company.slug
    return emp_data


@router.delete("/employees/{employee_id}")
async def delete_employee_endpoint(
    employee_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an employee (admin only)."""
    employee = await services.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Admin can only delete employees from their own company
    if employee.company_id != current_user["company_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Only admins can delete employees
    if current_user["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Only admins can delete employees")
    
    success = await services.delete_employee(db, employee_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete employee")
    
    return {"message": "Employee deleted successfully", "employee_id": employee_id}


# ========== Branding Routes ==========

@router.get("/company/{company_id}/branding")
async def get_company_branding(
    company_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get company branding settings (admin only)."""
    # Verify user owns this company
    if company_id != current_user["company_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    company = await services.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "brand_color": company.brand_color or "#3B82F6",
        "logo_url": company.logo_url,
        "company_name": company.name,
        "slug": company.slug,
    }


@router.put("/company/{company_id}/branding")
async def update_company_branding(
    company_id: uuid.UUID,
    branding_update: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update company branding settings (admin only)."""
    # Verify user owns this company
    if company_id != current_user["company_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    company = await services.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Validate brand_color if provided
    if "brand_color" in branding_update:
        color = branding_update["brand_color"]
        if not isinstance(color, str) or (not color.startswith("#") or len(color) not in (7, 4)):
            raise HTTPException(status_code=400, detail="Invalid color format. Use hex format: #RGB or #RRGGBB")
    
    # Update company branding
    company = await services.update_company_branding(db, company_id, branding_update)
    
    return {
        "status": "updated",
        "brand_color": company.brand_color,
        "logo_url": company.logo_url,
        "message": "Branding updated successfully",
    }


# ========== Analytics Routes ==========

@router.post("/analytics/track")
async def track_analytics(
    event_data: models.AnalyticsEventCreate,
    company_slug: str = Query(...),
    employee_slug: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Track an analytics event (public, no auth required)."""
    employee = await services.get_employee_by_slug(db, company_slug, employee_slug)
    if not employee:
        raise HTTPException(status_code=404, detail="Card not found")
    
    event = await services.track_event(
        db,
        employee.company_id,
        employee.id,
        event_data,
    )
    
    return {"status": "tracked", "event_id": event.id}


@router.get("/analytics/company/{company_id}")
async def get_company_analytics(
    company_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get analytics for a company."""
    if current_user["company_id"] != company_id and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    events = await services.get_analytics_by_company(db, company_id, skip, limit)
    summary = await services.get_analytics_summary(db, company_id)
    
    return {
        "events": [models.AnalyticsResponse.from_orm(e) for e in events],
        "summary": summary,
    }


@router.get("/analytics/employee/{employee_id}")
async def get_employee_analytics(
    employee_id: uuid.UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=10000),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get analytics for an employee."""
    employee = await services.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if employee.company_id != current_user["company_id"] and current_user["role"] != "superadmin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    events = await services.get_analytics_by_employee(db, employee_id, skip, limit)
    
    return {
        "events": [models.AnalyticsResponse.from_orm(e) for e in events],
    }


# ========== vCard & QR Code Routes ==========

@router.get("/card/{company_slug}/{employee_slug}/vcard")
async def get_vcard(
    company_slug: str,
    employee_slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Download vCard file for a business card (RFC 3.0 format).
    
    This endpoint returns a .vcf file that can be imported into contacts apps.
    When accessed, it triggers a download of the vCard file.
    """
    # Get employee and verify card exists
    employee = await services.get_employee_by_slug(db, company_slug, employee_slug)
    if not employee:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Generate vCard content
    vcard_content = vcard_utils.generate_vcard(
        full_name=employee.full_name,
        job_title=employee.job_title,
        email=employee.email,
        phone=employee.phone,
        whatsapp=employee.whatsapp,
        company_name=employee.company.name if employee.company else None,
        photo_url=employee.photo_url,
        bio=employee.bio,
        social_links=employee.social_links,
    )
    
    # Track analytics event
    await services.track_event(
        db,
        employee.company_id,
        models.AnalyticsEventCreate(
            action="download_vcard",
        ),
        employee.id,
    )
    
    # Return as downloadable file
    filename = f"{employee.full_name.replace(' ', '_')}.vcf"
    return Response(
        content=vcard_content.encode('utf-8'),
        media_type="text/vcard; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )


@router.get("/card/{company_slug}/{employee_slug}/qr-vcard")
async def get_qr_vcard(
    company_slug: str,
    employee_slug: str,
    db: AsyncSession = Depends(get_db),
):
    """Generate QR code that links to vCard download.
    
    This endpoint generates a QR code image that, when scanned, directs users
    to the vCard download endpoint. Users can then save the contact to their device.
    
    The QR code is generated server-side and returned as a redirect to the QR Server API.
    """
    # Get employee and verify card exists
    employee = await services.get_employee_by_slug(db, company_slug, employee_slug)
    if not employee:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Build vCard URL using environment variables for dynamic configuration
    import os
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = os.getenv("API_PORT", "8000")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    PROTOCOL = "https" if ENVIRONMENT == "production" else "http"
    
    vcard_url = f"{PROTOCOL}://{API_HOST}:{API_PORT}/api/card/{company_slug}/{employee_slug}/vcard"
    
    # Generate QR code URL from QR Server API
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={urllib.parse.quote(vcard_url)}"
    
    # Track analytics event
    await services.track_event(
        db,
        employee.company_id,
        models.AnalyticsEventCreate(
            action="scan_qr",
        ),
        employee.id,
    )
    
    # Redirect to QR Server API to get the image
    return RedirectResponse(url=qr_image_url)


# ========== Subscription & Payment Routes ==========

@router.get("/subscriptions/plans")
async def get_subscription_plans():
    """Get all available subscription plans with pricing"""
    from subscription_config import (
        PLAN_FREE, PLAN_PROFESSIONAL, PLAN_ENTERPRISE,
        PLAN_PRICES_USD, PLAN_PRICES_KWD,
        PLAN_FEATURES, TRIAL_DAYS, CURRENCY_SYMBOLS
    )
    
    plans = [
        {
            "id": PLAN_FREE,
            "name": "Free",
            "description": "Perfect for getting started",
            "features": PLAN_FEATURES[PLAN_FREE],
            "pricing": {
                "USD": {
                    "monthly": 0,
                    "yearly": 0,
                    "symbol": CURRENCY_SYMBOLS["USD"],
                },
                "KWD": {
                    "monthly": 0,
                    "yearly": 0,
                    "symbol": CURRENCY_SYMBOLS["KWD"],
                },
            },
            "trial_days": 0,
        },
        {
            "id": PLAN_PROFESSIONAL,
            "name": "Professional",
            "description": "For growing teams",
            "features": PLAN_FEATURES[PLAN_PROFESSIONAL],
            "pricing": {
                "USD": {
                    "monthly": PLAN_PRICES_USD[PLAN_PROFESSIONAL]["monthly"],
                    "yearly": PLAN_PRICES_USD[PLAN_PROFESSIONAL]["yearly"],
                    "symbol": CURRENCY_SYMBOLS["USD"],
                },
                "KWD": {
                    "monthly": PLAN_PRICES_KWD[PLAN_PROFESSIONAL]["monthly"],
                    "yearly": PLAN_PRICES_KWD[PLAN_PROFESSIONAL]["yearly"],
                    "symbol": CURRENCY_SYMBOLS["KWD"],
                },
            },
            "trial_days": TRIAL_DAYS,
        },
        {
            "id": PLAN_ENTERPRISE,
            "name": "Enterprise",
            "description": "For large organizations",
            "features": PLAN_FEATURES[PLAN_ENTERPRISE],
            "pricing": {
                "USD": {
                    "monthly": PLAN_PRICES_USD[PLAN_ENTERPRISE]["monthly"],
                    "yearly": PLAN_PRICES_USD[PLAN_ENTERPRISE]["yearly"],
                    "symbol": CURRENCY_SYMBOLS["USD"],
                },
                "KWD": {
                    "monthly": PLAN_PRICES_KWD[PLAN_ENTERPRISE]["monthly"],
                    "yearly": PLAN_PRICES_KWD[PLAN_ENTERPRISE]["yearly"],
                    "symbol": CURRENCY_SYMBOLS["KWD"],
                },
            },
            "trial_days": TRIAL_DAYS,
        },
    ]
    
    return {"plans": plans}


@router.get("/subscriptions/current")
async def get_current_subscription(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current subscription for authenticated user's company"""
    company_id = current_user["company_id"]
    
    if not company_id:
        raise HTTPException(status_code=404, detail="Company not found")
    
    from subscription_service import get_active_subscription, check_employee_limit
    
    subscription = await get_active_subscription(db, company_id)
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")
    
    # Get employee limits
    limit_info = await check_employee_limit(db, company_id)
    
    return {
        "id": subscription.id,
        "plan": subscription.plan,
        "status": subscription.status,
        "billing_cycle": subscription.billing_cycle,
        "currency": subscription.currency,
        "amount": float(subscription.amount) if subscription.amount else 0,
        "current_period_start": subscription.current_period_start,
        "current_period_end": subscription.current_period_end,
        "cancel_at": subscription.cancel_at,
        "trial_end": subscription.trial_end,
        "employee_count": limit_info["current"],
        "employee_limit": limit_info["limit"],
        "can_add_employee": limit_info["can_add"],
    }


@router.post("/subscriptions/create-checkout")
async def create_checkout_session(
    checkout_data: dict = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create Stripe checkout session for subscription"""
    company_id = current_user["company_id"]
    plan = checkout_data.get("plan")
    billing_cycle = checkout_data.get("billing_cycle", "monthly")
    currency = checkout_data.get("currency", "USD")
    
    if not company_id:
        raise HTTPException(status_code=400, detail="Company not found")
    
    if plan not in ["professional", "enterprise"]:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    # Get company
    company = await services.get_company_by_id(db, company_id)
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get or create Stripe customer
    from subscription_service import get_active_subscription
    from stripe_service import StripeService
    from subscription_config import STRIPE_PRICE_IDS, TRIAL_DAYS
    
    subscription = await get_active_subscription(db, company_id)
    stripe_service = StripeService()
    
    if subscription and subscription.stripe_customer_id:
        customer_id = subscription.stripe_customer_id
    else:
        # Create new customer
        user = current_user["user"]
        customer = await stripe_service.create_customer(
            email=user.email,
            company_name=company.name,
            company_id=str(company_id),
        )
        customer_id = customer.id
    
    # Get price ID
    price_key = f"{plan}_{billing_cycle}"
    price_id = STRIPE_PRICE_IDS.get(currency, {}).get(price_key)
    
    if not price_id:
        raise HTTPException(status_code=400, detail="Price not found for this plan")
    
    # Create checkout session
    success_url = checkout_data.get("success_url", f"{os.getenv('FRONTEND_HOST')}/company-admin/subscription/success")
    cancel_url = checkout_data.get("cancel_url", f"{os.getenv('FRONTEND_HOST')}/company-admin/subscription/cancel")
    
    session = await stripe_service.create_checkout_session(
        customer_id=customer_id,
        price_id=price_id,
        success_url=success_url,
        cancel_url=cancel_url,
        trial_days=TRIAL_DAYS,
        metadata={
            "company_id": str(company_id),
            "plan": plan,
            "billing_cycle": billing_cycle,
        }
    )
    
    return {
        "checkout_url": session.url,
        "session_id": session.id,
    }


@router.post("/subscriptions/cancel")
async def cancel_subscription_endpoint(
    cancel_data: dict = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel subscription"""
    company_id = current_user["company_id"]
    at_period_end = cancel_data.get("at_period_end", True)
    
    if not company_id:
        raise HTTPException(status_code=400, detail="Company not found")
    
    if current_user["role"] not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Only admins can cancel subscriptions")
    
    from subscription_service import cancel_subscription
    
    try:
        subscription = await cancel_subscription(db, company_id, at_period_end)
        
        return {
            "message": "Subscription canceled successfully",
            "subscription": {
                "plan": subscription.plan,
                "status": subscription.status,
                "cancel_at": subscription.cancel_at,
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/subscriptions/portal")
async def create_portal_session(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create Stripe customer portal session"""
    company_id = current_user["company_id"]
    
    if not company_id:
        raise HTTPException(status_code=400, detail="Company not found")
    
    from subscription_service import get_active_subscription
    from stripe_service import StripeService
    
    subscription = await get_active_subscription(db, company_id)
    
    if not subscription or not subscription.stripe_customer_id:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    stripe_service = StripeService()
    return_url = f"{os.getenv('FRONTEND_HOST')}/company-admin/subscription"
    
    portal_session = await stripe_service.create_portal_session(
        customer_id=subscription.stripe_customer_id,
        return_url=return_url,
    )
    
    return {
        "portal_url": portal_session.url,
    }


@router.get("/subscriptions/invoices")
async def get_invoices(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get invoices for company"""
    company_id = current_user["company_id"]
    
    if not company_id:
        raise HTTPException(status_code=400, detail="Company not found")
    
    from subscription_service import list_invoices
    
    invoices = await list_invoices(db, company_id, limit=20)
    
    return {
        "invoices": [
            {
                "id": inv.id,
                "amount": float(inv.amount),
                "currency": inv.currency,
                "status": inv.status,
                "paid_at": inv.paid_at,
                "invoice_pdf_url": inv.invoice_pdf_url,
                "hosted_invoice_url": inv.hosted_invoice_url,
                "created_at": inv.created_at,
            }
            for inv in invoices
        ]
    }


@router.post("/webhooks/stripe", include_in_schema=False)
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Stripe webhooks"""
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    from stripe_service import StripeService
    from subscription_service import create_paid_subscription, create_invoice_record
    
    try:
        # Verify webhook signature
        event = StripeService.verify_webhook_signature(payload, signature)
        
        # Handle different event types
        if event["type"] == "checkout.session.completed":
            # Subscription created successfully
            session = event["data"]["object"]
            metadata = session.get("metadata", {})
            company_id = uuid.UUID(metadata.get("company_id"))
            plan = metadata.get("plan")
            billing_cycle = metadata.get("billing_cycle")
            
            # Get subscription details from Stripe
            subscription_id = session.get("subscription")
            stripe_service = StripeService()
            stripe_subscription = await stripe_service.get_subscription(subscription_id)
            
            # Create subscription in database
            await create_paid_subscription(
                db,
                company_id=company_id,
                plan=plan,
                billing_cycle=billing_cycle,
                stripe_customer_id=session.get("customer"),
                stripe_subscription_id=subscription_id,
                stripe_price_id=stripe_subscription["items"]["data"][0]["price"]["id"],
                currency=session.get("currency", "usd").upper(),
                amount=session.get("amount_total", 0) / 100,
            )
        
        elif event["type"] == "invoice.paid":
            # Invoice paid successfully
            invoice = event["data"]["object"]
            customer_id = invoice.get("customer")
            
            # Find subscription by Stripe customer ID
            result = await db.execute(
                select(db.Subscription)
                .where(db.Subscription.stripe_customer_id == customer_id)
                .where(db.Subscription.status.in_(["active", "trialing"]))
            )
            subscription = result.scalar_one_or_none()
            
            if subscription:
                # Create invoice record
                await create_invoice_record(
                    db,
                    company_id=subscription.company_id,
                    subscription_id=subscription.id,
                    stripe_invoice_id=invoice.get("id"),
                    amount=invoice.get("amount_paid", 0) / 100,
                    currency=invoice.get("currency", "usd").upper(),
                    status="paid",
                    invoice_pdf_url=invoice.get("invoice_pdf"),
                    hosted_invoice_url=invoice.get("hosted_invoice_url"),
                    paid_at=datetime.fromtimestamp(invoice.get("status_transitions", {}).get("paid_at", 0)),
                )
        
        elif event["type"] == "customer.subscription.updated":
            # Subscription updated (renewed, upgraded, etc.)
            subscription = event["data"]["object"]
            stripe_subscription_id = subscription.get("id")
            
            # Update subscription in database
            result = await db.execute(
                select(db.Subscription)
                .where(db.Subscription.stripe_subscription_id == stripe_subscription_id)
            )
            db_subscription = result.scalar_one_or_none()
            
            if db_subscription:
                db_subscription.status = subscription.get("status")
                db_subscription.current_period_start = datetime.fromtimestamp(subscription.get("current_period_start"))
                db_subscription.current_period_end = datetime.fromtimestamp(subscription.get("current_period_end"))
                
                if subscription.get("cancel_at"):
                    db_subscription.cancel_at = datetime.fromtimestamp(subscription.get("cancel_at"))
                
                await db.commit()
        
        elif event["type"] == "customer.subscription.deleted":
            # Subscription canceled/expired
            subscription = event["data"]["object"]
            stripe_subscription_id = subscription.get("id")
            
            # Update subscription in database
            result = await db.execute(
                select(db.Subscription)
                .where(db.Subscription.stripe_subscription_id == stripe_subscription_id)
            )
            db_subscription = result.scalar_one_or_none()
            
            if db_subscription:
                db_subscription.status = "canceled"
                db_subscription.active = False
                db_subscription.ended_at = datetime.utcnow()
                db_subscription.plan = "free"  # Downgrade to free
                
                await db.commit()
        
        return {"status": "success"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
