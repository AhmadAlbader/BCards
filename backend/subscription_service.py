"""
Subscription Management Service
Business logic for handling subscriptions
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

import database_models as db
from subscription_config import (
    PLAN_FREE, PLAN_PROFESSIONAL, PLAN_ENTERPRISE,
    PLAN_LIMITS, TRIAL_DAYS, get_plan_limits
)
from stripe_service import StripeService


async def create_free_subscription(
    session: AsyncSession,
    company_id: uuid.UUID
) -> db.Subscription:
    """
    Create a free subscription for a new company
    
    Args:
        session: Database session
        company_id: Company ID
        
    Returns:
        Subscription object
    """
    subscription = db.Subscription(
        company_id=company_id,
        plan=PLAN_FREE,
        status="active",
        active=True,
        billing_cycle=None,
        currency="USD",
        amount=0,
    )
    
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    
    return subscription


async def get_active_subscription(
    session: AsyncSession,
    company_id: uuid.UUID
) -> Optional[db.Subscription]:
    """
    Get active subscription for a company
    
    Args:
        session: Database session
        company_id: Company ID
        
    Returns:
        Subscription or None
    """
    result = await session.execute(
        select(db.Subscription)
        .where(db.Subscription.company_id == company_id)
        .where(db.Subscription.status.in_(["active", "trialing"]))
        .order_by(db.Subscription.created_at.desc())
    )
    
    return result.scalar_one_or_none()


async def check_subscription_active(
    session: AsyncSession,
    company_id: uuid.UUID
) -> bool:
    """
    Check if company has active subscription
    
    Args:
        session: Database session
        company_id: Company ID
        
    Returns:
        True if active, False otherwise
    """
    subscription = await get_active_subscription(session, company_id)
    
    if not subscription:
        return False
    
    # Check if subscription is past due
    if subscription.status == "past_due":
        return False
    
    # Check if ended
    if subscription.ended_at and subscription.ended_at < datetime.utcnow():
        return False
    
    return True


async def check_employee_limit(
    session: AsyncSession,
    company_id: uuid.UUID
) -> Dict[str, Any]:
    """
    Check employee limit for company
    
    Args:
        session: Database session
        company_id: Company ID
        
    Returns:
        Dict with current count, limit, and can_add flag
    """
    # Get subscription
    subscription = await get_active_subscription(session, company_id)
    
    if not subscription:
        # Default to free plan limits
        plan = PLAN_FREE
    else:
        plan = subscription.plan
    
    # Get plan limits
    limits = get_plan_limits(plan)
    employee_limit = limits["employees"]
    
    # Count current employees
    result = await session.execute(
        select(func.count(db.Employee.id))
        .where(db.Employee.company_id == company_id)
    )
    current_count = result.scalar()
    
    return {
        "current": current_count,
        "limit": employee_limit,
        "can_add": current_count < employee_limit,
        "plan": plan,
    }


async def enforce_employee_limit(
    session: AsyncSession,
    company_id: uuid.UUID
) -> None:
    """
    Enforce employee limit, raise exception if exceeded
    
    Args:
        session: Database session
        company_id: Company ID
        
    Raises:
        ValueError: If limit exceeded
    """
    limit_info = await check_employee_limit(session, company_id)
    
    if not limit_info["can_add"]:
        raise ValueError(
            f"Employee limit reached ({limit_info['current']}/{limit_info['limit']}). "
            f"Upgrade your plan to add more employees."
        )


async def create_paid_subscription(
    session: AsyncSession,
    company_id: uuid.UUID,
    plan: str,
    billing_cycle: str,
    stripe_customer_id: str,
    stripe_subscription_id: str,
    stripe_price_id: str,
    currency: str,
    amount: float
) -> db.Subscription:
    """
    Create a paid subscription after successful payment
    
    Args:
        session: Database session
        company_id: Company ID
        plan: Plan name
        billing_cycle: monthly or yearly
        stripe_customer_id: Stripe customer ID
        stripe_subscription_id: Stripe subscription ID
        stripe_price_id: Stripe price ID
        currency: Currency code
        amount: Amount paid
        
    Returns:
        Subscription object
    """
    # Cancel existing subscription if any
    existing = await get_active_subscription(session, company_id)
    if existing:
        existing.status = "canceled"
        existing.canceled_at = datetime.utcnow()
        existing.active = False
    
    # Create new subscription
    subscription = db.Subscription(
        company_id=company_id,
        plan=plan,
        billing_cycle=billing_cycle,
        status="active",
        active=True,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_id=stripe_subscription_id,
        stripe_price_id=stripe_price_id,
        currency=currency,
        amount=amount,
        current_period_start=datetime.utcnow(),
    )
    
    session.add(subscription)
    await session.commit()
    await session.refresh(subscription)
    
    return subscription


async def cancel_subscription(
    session: AsyncSession,
    company_id: uuid.UUID,
    at_period_end: bool = True
) -> db.Subscription:
    """
    Cancel a subscription
    
    Args:
        session: Database session
        company_id: Company ID
        at_period_end: Cancel at end of billing period
        
    Returns:
        Updated subscription
    """
    subscription = await get_active_subscription(session, company_id)
    
    if not subscription:
        raise ValueError("No active subscription found")
    
    # Cancel in Stripe if paid subscription
    if subscription.stripe_subscription_id:
        stripe_service = StripeService()
        await stripe_service.cancel_subscription(
            subscription.stripe_subscription_id,
            at_period_end=at_period_end
        )
    
    # Update database
    if at_period_end:
        subscription.cancel_at = subscription.current_period_end
        subscription.status = "active"  # Still active until period end
    else:
        subscription.status = "canceled"
        subscription.canceled_at = datetime.utcnow()
        subscription.active = False
        
        # Downgrade to free plan
        subscription.plan = PLAN_FREE
    
    await session.commit()
    await session.refresh(subscription)
    
    return subscription


async def upgrade_subscription(
    session: AsyncSession,
    company_id: uuid.UUID,
    new_plan: str,
    new_billing_cycle: str,
    new_price_id: str
) -> db.Subscription:
    """
    Upgrade subscription to new plan
    
    Args:
        session: Database session
        company_id: Company ID
        new_plan: New plan name
        new_billing_cycle: New billing cycle
        new_price_id: New Stripe price ID
        
    Returns:
        Updated subscription
    """
    subscription = await get_active_subscription(session, company_id)
    
    if not subscription:
        raise ValueError("No active subscription found")
    
    if not subscription.stripe_subscription_id:
        raise ValueError("Cannot upgrade free plan this way")
    
    # Update in Stripe
    stripe_service = StripeService()
    await stripe_service.update_subscription(
        subscription.stripe_subscription_id,
        new_price_id,
        proration_behavior="always_invoice"
    )
    
    # Update database
    subscription.plan = new_plan
    subscription.billing_cycle = new_billing_cycle
    subscription.stripe_price_id = new_price_id
    
    await session.commit()
    await session.refresh(subscription)
    
    return subscription


async def get_subscription_features(
    session: AsyncSession,
    company_id: uuid.UUID
) -> Dict[str, Any]:
    """
    Get available features for company's subscription
    
    Args:
        session: Database session
        company_id: Company ID
        
    Returns:
        Dict of available features
    """
    subscription = await get_active_subscription(session, company_id)
    
    if not subscription:
        plan = PLAN_FREE
    else:
        plan = subscription.plan
    
    return get_plan_limits(plan)


async def create_invoice_record(
    session: AsyncSession,
    company_id: uuid.UUID,
    subscription_id: uuid.UUID,
    stripe_invoice_id: str,
    amount: float,
    currency: str,
    status: str,
    invoice_pdf_url: Optional[str] = None,
    hosted_invoice_url: Optional[str] = None,
    paid_at: Optional[datetime] = None
) -> db.Invoice:
    """
    Create invoice record in database
    
    Args:
        session: Database session
        company_id: Company ID
        subscription_id: Subscription ID
        stripe_invoice_id: Stripe invoice ID
        amount: Invoice amount
        currency: Currency code
        status: Invoice status
        invoice_pdf_url: PDF URL
        hosted_invoice_url: Hosted invoice URL
        paid_at: Payment date
        
    Returns:
        Invoice object
    """
    invoice = db.Invoice(
        company_id=company_id,
        subscription_id=subscription_id,
        stripe_invoice_id=stripe_invoice_id,
        amount=amount,
        currency=currency,
        status=status,
        invoice_pdf_url=invoice_pdf_url,
        hosted_invoice_url=hosted_invoice_url,
        paid_at=paid_at,
    )
    
    session.add(invoice)
    await session.commit()
    await session.refresh(invoice)
    
    return invoice


async def list_invoices(
    session: AsyncSession,
    company_id: uuid.UUID,
    limit: int = 10
) -> list:
    """
    Get invoices for a company
    
    Args:
        session: Database session
        company_id: Company ID
        limit: Maximum number of invoices
        
    Returns:
        List of invoices
    """
    result = await session.execute(
        select(db.Invoice)
        .where(db.Invoice.company_id == company_id)
        .order_by(db.Invoice.created_at.desc())
        .limit(limit)
    )
    
    return result.scalars().all()
