from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
import datetime
import uuid


# ========== Pydantic Models (API Request/Response) ==========

class CompanyCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    logo_url: Optional[str] = None
    brand_color: Optional[str] = None


class CompanyResponse(BaseModel):
    id: uuid.UUID
    name: str
    domain: Optional[str]
    logo_url: Optional[str]
    brand_color: Optional[str]
    slug: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class EmployeeCreate(BaseModel):
    full_name: str
    job_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    job_title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    photo_url: Optional[str] = None
    bio: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None


class EmployeeResponse(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    full_name: str
    job_title: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    whatsapp: Optional[str]
    photo_url: Optional[str]
    bio: Optional[str]
    social_links: Optional[Dict[str, str]]
    public_slug: str
    last_updated: datetime.datetime
    company_slug: Optional[str] = None

    class Config:
        from_attributes = True


class BusinessCardResponse(BaseModel):
    employee_id: uuid.UUID
    employee_name: str
    company_name: str
    company_id: uuid.UUID
    job_title: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    whatsapp: Optional[str]
    bio: Optional[str]
    photo_url: Optional[str]
    social_links: Optional[Dict[str, str]]
    qr_code: Optional[str]
    vcard_url: Optional[str]
    company_logo: Optional[str]
    company_brand_color: Optional[str]


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "admin"  # admin | employee


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: uuid.UUID
    company_id: Optional[uuid.UUID]
    role: str


class SubscriptionResponse(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    plan: str
    active: bool
    started_at: datetime.datetime

    class Config:
        from_attributes = True


class AnalyticsEventCreate(BaseModel):
    device: Optional[str] = None
    region: Optional[str] = None
    action: str  # view | call | whatsapp | email | download_vcard | scan_qr


class AnalyticsResponse(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    company_id: uuid.UUID
    timestamp: datetime.datetime
    device: Optional[str]
    region: Optional[str]
    action: str

    class Config:
        from_attributes = True
