"""
Subscription Plans Configuration
Easily modify pricing and limits here
"""

# Plan Names
PLAN_FREE = "free"
PLAN_PROFESSIONAL = "professional"
PLAN_ENTERPRISE = "enterprise"

# Plan Limits
PLAN_LIMITS = {
    PLAN_FREE: {
        "employees": 2,
        "analytics_days": 30,
        "custom_logo": False,
        "api_access": False,
        "priority_support": False,
        "white_label": False,
        "custom_domain": False,
    },
    PLAN_PROFESSIONAL: {
        "employees": 50,
        "analytics_days": 365,
        "custom_logo": True,
        "api_access": False,
        "priority_support": True,
        "white_label": False,
        "custom_domain": False,
    },
    PLAN_ENTERPRISE: {
        "employees": 999999,  # Unlimited
        "analytics_days": 9999,  # Unlimited
        "custom_logo": True,
        "api_access": True,
        "priority_support": True,
        "white_label": True,
        "custom_domain": True,
    },
}

# Pricing (USD)
PLAN_PRICES_USD = {
    PLAN_FREE: {
        "monthly": 0,
        "yearly": 0,
    },
    PLAN_PROFESSIONAL: {
        "monthly": 29.00,
        "yearly": 290.00,  # Save 17% (2 months free)
    },
    PLAN_ENTERPRISE: {
        "monthly": 99.00,
        "yearly": 990.00,  # Save 17% (2 months free)
    },
}

# Pricing (KWD - Kuwaiti Dinar)
PLAN_PRICES_KWD = {
    PLAN_FREE: {
        "monthly": 0,
        "yearly": 0,
    },
    PLAN_PROFESSIONAL: {
        "monthly": 8.90,
        "yearly": 89.00,
    },
    PLAN_ENTERPRISE: {
        "monthly": 30.50,
        "yearly": 305.00,
    },
}

# Stripe Price IDs (set these after creating prices in Stripe Dashboard)
STRIPE_PRICE_IDS = {
    "USD": {
        f"{PLAN_PROFESSIONAL}_monthly": "price_professional_usd_monthly",
        f"{PLAN_PROFESSIONAL}_yearly": "price_professional_usd_yearly",
        f"{PLAN_ENTERPRISE}_monthly": "price_enterprise_usd_monthly",
        f"{PLAN_ENTERPRISE}_yearly": "price_enterprise_usd_yearly",
    },
    "KWD": {
        f"{PLAN_PROFESSIONAL}_monthly": "price_professional_kwd_monthly",
        f"{PLAN_PROFESSIONAL}_yearly": "price_professional_kwd_yearly",
        f"{PLAN_ENTERPRISE}_monthly": "price_enterprise_kwd_monthly",
        f"{PLAN_ENTERPRISE}_yearly": "price_enterprise_kwd_yearly",
    },
}

# Trial Configuration
TRIAL_DAYS = 3

# Plan Features Display (for frontend)
PLAN_FEATURES = {
    PLAN_FREE: [
        "Up to 2 employees",
        "Basic branding (color only)",
        "Basic analytics (30 days)",
        "QR codes & vCards",
        "Email support",
    ],
    PLAN_PROFESSIONAL: [
        "Up to 50 employees",
        "Full branding (color + logo)",
        "Advanced analytics (unlimited)",
        "QR codes & vCards",
        "Priority email support",
        "Custom domain support",
    ],
    PLAN_ENTERPRISE: [
        "Unlimited employees",
        "Full branding + white label",
        "Advanced analytics + exports",
        "API access",
        "Priority support",
        "Custom domain",
        "Dedicated account manager",
    ],
}

# Currency Configuration
SUPPORTED_CURRENCIES = ["USD", "KWD"]
DEFAULT_CURRENCY = "USD"

# Currency Symbols
CURRENCY_SYMBOLS = {
    "USD": "$",
    "KWD": "KD",
}

# Currency Names
CURRENCY_NAMES = {
    "USD": "US Dollar",
    "KWD": "Kuwaiti Dinar",
}


def get_plan_price(plan: str, billing_cycle: str, currency: str = "USD"):
    """Get price for a plan in specific currency"""
    if currency == "USD":
        return PLAN_PRICES_USD.get(plan, {}).get(billing_cycle, 0)
    elif currency == "KWD":
        return PLAN_PRICES_KWD.get(plan, {}).get(billing_cycle, 0)
    return 0


def get_plan_limits(plan: str):
    """Get limits for a specific plan"""
    return PLAN_LIMITS.get(plan, PLAN_LIMITS[PLAN_FREE])


def format_price(amount: float, currency: str = "USD"):
    """Format price with currency symbol"""
    symbol = CURRENCY_SYMBOLS.get(currency, "$")
    return f"{symbol}{amount:.2f}"
