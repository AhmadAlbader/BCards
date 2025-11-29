from sqlalchemy import Column, String, Boolean, DateTime, JSON, ForeignKey, Text, func, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, nullable=True)
    logo_url = Column(Text, nullable=True)
    brand_color = Column(String(7), nullable=True)
    slug = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")
    users = relationship("User", back_populates="company", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="company", cascade="all, delete-orphan")
    analytics = relationship("AnalyticsEvent", back_populates="company", cascade="all, delete-orphan")
    payment_methods = relationship("PaymentMethod", back_populates="company", cascade="all, delete-orphan")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    whatsapp = Column(String(20), nullable=True)
    photo_url = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    social_links = Column(JSON, nullable=True, default={})
    public_slug = Column(String(255), unique=True, nullable=False)
    last_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    company = relationship("Company", back_populates="employees")
    cards = relationship("Card", back_populates="employee", cascade="all, delete-orphan")
    analytics = relationship("AnalyticsEvent", back_populates="employee", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    qr_code = Column(Text, nullable=True)
    vcard_url = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    employee = relationship("Employee", back_populates="cards")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default="employee")  # superadmin | admin | employee
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    company = relationship("Company", back_populates="users")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    
    # Plan Information
    plan = Column(String(50), nullable=False)  # free | professional | enterprise
    billing_cycle = Column(String(20), nullable=True)  # monthly | yearly
    status = Column(String(50), default="active")  # active | canceled | past_due | trialing
    
    # Stripe Integration
    stripe_customer_id = Column(String(255), nullable=True, unique=True)
    stripe_subscription_id = Column(String(255), nullable=True, unique=True)
    stripe_price_id = Column(String(255), nullable=True)
    
    # Payment Information
    payment_method = Column(String(50), nullable=True)  # card | paypal | bank_transfer
    currency = Column(String(3), default="USD")  # USD | KWD
    amount = Column(Numeric(10, 2), nullable=True)
    
    # Dates
    trial_end = Column(DateTime, nullable=True)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Legacy
    active = Column(Boolean, default=True)  # Kept for backward compatibility

    # Relationships
    company = relationship("Company", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")
    payment_methods = relationship("PaymentMethod", back_populates="company", foreign_keys="PaymentMethod.company_id")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True)
    
    # Stripe Integration
    stripe_invoice_id = Column(String(255), nullable=True, unique=True)
    stripe_payment_intent_id = Column(String(255), nullable=True)
    
    # Invoice Details
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(String(50), nullable=False)  # paid | pending | failed | draft
    
    # URLs
    invoice_pdf_url = Column(Text, nullable=True)
    hosted_invoice_url = Column(Text, nullable=True)
    
    # Dates
    paid_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    
    # Stripe Integration
    stripe_payment_method_id = Column(String(255), nullable=True, unique=True)
    
    # Payment Method Details
    type = Column(String(50), nullable=False)  # card | bank_account
    brand = Column(String(50), nullable=True)  # visa | mastercard | amex
    last4 = Column(String(4), nullable=True)
    exp_month = Column(String(2), nullable=True)
    exp_year = Column(String(4), nullable=True)
    
    # Status
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Dates
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    company = relationship("Company", foreign_keys=[company_id])


class AnalyticsEvent(Base):
    __tablename__ = "analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
    device = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    action = Column(String(50), nullable=False)  # view | call | whatsapp | email | download_vcard | scan_qr
    ip_address = Column(String(45), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="analytics")
    employee = relationship("Employee", back_populates="analytics")
