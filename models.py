from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime


class Company(BaseModel):
    id: Optional[int]
    name: str
    domain: Optional[str] = None
    created_at: datetime.datetime = datetime.datetime.utcnow()


class BusinessCard(BaseModel):
    id: Optional[int]
    company_id: int
    name: str
    title: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime.datetime = datetime.datetime.utcnow()


class User(BaseModel):
    id: Optional[int]
    company_id: int
    email: EmailStr
    full_name: Optional[str] = None


class Subscription(BaseModel):
    id: Optional[int]
    company_id: int
    plan: str
    active: bool = True
    started_at: datetime.datetime = datetime.datetime.utcnow()
