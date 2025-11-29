"""
Stripe Payment Integration Service
Handles all Stripe API interactions
"""
import os
import stripe
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Webhook secret for signature verification
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


class StripeService:
    """Service for handling Stripe operations"""

    @staticmethod
    async def create_customer(
        email: str,
        company_name: str,
        company_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.Customer:
        """
        Create a Stripe customer
        
        Args:
            email: Customer email
            company_name: Company name
            company_id: Internal company ID
            metadata: Additional metadata
            
        Returns:
            Stripe Customer object
        """
        customer_metadata = metadata or {}
        customer_metadata.update({
            "company_id": str(company_id),
            "company_name": company_name,
        })
        
        customer = stripe.Customer.create(
            email=email,
            name=company_name,
            metadata=customer_metadata,
        )
        
        return customer

    @staticmethod
    async def create_checkout_session(
        customer_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
        trial_days: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.checkout.Session:
        """
        Create a Stripe Checkout session
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel
            trial_days: Number of trial days
            metadata: Additional metadata
            
        Returns:
            Stripe Checkout Session
        """
        session_params = {
            "customer": customer_id,
            "payment_method_types": ["card"],
            "line_items": [
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            "mode": "subscription",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "metadata": metadata or {},
        }
        
        # Add trial period if specified
        if trial_days > 0:
            session_params["subscription_data"] = {
                "trial_period_days": trial_days,
                "metadata": metadata or {},
            }
        
        session = stripe.checkout.Session.create(**session_params)
        return session

    @staticmethod
    async def create_subscription(
        customer_id: str,
        price_id: str,
        trial_days: int = 0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> stripe.Subscription:
        """
        Create a subscription directly (without checkout)
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            trial_days: Number of trial days
            metadata: Additional metadata
            
        Returns:
            Stripe Subscription object
        """
        subscription_params = {
            "customer": customer_id,
            "items": [{"price": price_id}],
            "metadata": metadata or {},
        }
        
        if trial_days > 0:
            trial_end = datetime.utcnow() + timedelta(days=trial_days)
            subscription_params["trial_end"] = int(trial_end.timestamp())
        
        subscription = stripe.Subscription.create(**subscription_params)
        return subscription

    @staticmethod
    async def cancel_subscription(
        subscription_id: str,
        at_period_end: bool = True
    ) -> stripe.Subscription:
        """
        Cancel a subscription
        
        Args:
            subscription_id: Stripe subscription ID
            at_period_end: If True, cancel at end of billing period
            
        Returns:
            Updated Stripe Subscription
        """
        if at_period_end:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
        else:
            subscription = stripe.Subscription.delete(subscription_id)
        
        return subscription

    @staticmethod
    async def reactivate_subscription(subscription_id: str) -> stripe.Subscription:
        """
        Reactivate a canceled subscription
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            Updated Stripe Subscription
        """
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
        return subscription

    @staticmethod
    async def update_subscription(
        subscription_id: str,
        new_price_id: str,
        proration_behavior: str = "always_invoice"
    ) -> stripe.Subscription:
        """
        Update subscription to new plan (upgrade/downgrade)
        
        Args:
            subscription_id: Stripe subscription ID
            new_price_id: New Stripe price ID
            proration_behavior: How to handle prorations
            
        Returns:
            Updated Stripe Subscription
        """
        subscription = stripe.Subscription.retrieve(subscription_id)
        
        updated_subscription = stripe.Subscription.modify(
            subscription_id,
            items=[{
                "id": subscription["items"]["data"][0].id,
                "price": new_price_id,
            }],
            proration_behavior=proration_behavior,
        )
        
        return updated_subscription

    @staticmethod
    async def get_subscription(subscription_id: str) -> stripe.Subscription:
        """Get subscription details"""
        return stripe.Subscription.retrieve(subscription_id)

    @staticmethod
    async def get_customer(customer_id: str) -> stripe.Customer:
        """Get customer details"""
        return stripe.Customer.retrieve(customer_id)

    @staticmethod
    async def list_invoices(customer_id: str, limit: int = 10) -> list:
        """Get customer invoices"""
        invoices = stripe.Invoice.list(
            customer=customer_id,
            limit=limit
        )
        return invoices.data

    @staticmethod
    async def get_upcoming_invoice(customer_id: str) -> Optional[stripe.Invoice]:
        """Get upcoming invoice preview"""
        try:
            invoice = stripe.Invoice.upcoming(customer=customer_id)
            return invoice
        except stripe.error.InvalidRequestError:
            return None

    @staticmethod
    def verify_webhook_signature(payload: bytes, signature: str) -> Dict[str, Any]:
        """
        Verify Stripe webhook signature
        
        Args:
            payload: Raw request body
            signature: Stripe signature header
            
        Returns:
            Parsed event data
            
        Raises:
            ValueError: If signature is invalid
        """
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            raise ValueError(f"Invalid payload: {e}")
        except stripe.error.SignatureVerificationError as e:
            raise ValueError(f"Invalid signature: {e}")

    @staticmethod
    async def create_portal_session(
        customer_id: str,
        return_url: str
    ) -> stripe.billing_portal.Session:
        """
        Create a customer portal session for managing subscription
        
        Args:
            customer_id: Stripe customer ID
            return_url: URL to return to after portal
            
        Returns:
            Portal session with URL
        """
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return session

    @staticmethod
    async def create_payment_method(
        customer_id: str,
        payment_method_id: str
    ) -> stripe.PaymentMethod:
        """
        Attach payment method to customer
        
        Args:
            customer_id: Stripe customer ID
            payment_method_id: Payment method ID from frontend
            
        Returns:
            Payment method object
        """
        payment_method = stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
        )
        
        # Set as default
        stripe.Customer.modify(
            customer_id,
            invoice_settings={
                "default_payment_method": payment_method_id,
            },
        )
        
        return payment_method
