"""
Migration script to update database schema for subscription system
Run this script to add new tables and modify existing ones for Stripe integration

Usage:
    python migrate_subscriptions.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import text
from database import engine


async def run_migration():
    """Run database migration for subscription system"""
    
    print("🚀 Starting subscription system migration...")
    print("=" * 60)
    
    async with engine.begin() as conn:
        
        # 1. Update subscriptions table
        print("\n📝 Step 1: Updating subscriptions table...")
        try:
            await conn.execute(text("""
                ALTER TABLE subscriptions 
                ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR,
                ADD COLUMN IF NOT EXISTS stripe_subscription_id VARCHAR,
                ADD COLUMN IF NOT EXISTS stripe_price_id VARCHAR,
                ADD COLUMN IF NOT EXISTS payment_method VARCHAR(50),
                ADD COLUMN IF NOT EXISTS currency VARCHAR(3) DEFAULT 'USD',
                ADD COLUMN IF NOT EXISTS amount NUMERIC(10, 2) DEFAULT 0.00,
                ADD COLUMN IF NOT EXISTS billing_cycle VARCHAR(20) DEFAULT 'monthly',
                ADD COLUMN IF NOT EXISTS current_period_start TIMESTAMP,
                ADD COLUMN IF NOT EXISTS current_period_end TIMESTAMP,
                ADD COLUMN IF NOT EXISTS cancel_at TIMESTAMP,
                ADD COLUMN IF NOT EXISTS canceled_at TIMESTAMP;
            """))
            
            # Add indexes for performance
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe_customer 
                ON subscriptions(stripe_customer_id);
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_subscriptions_stripe_subscription 
                ON subscriptions(stripe_subscription_id);
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_subscriptions_company 
                ON subscriptions(company_id);
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_subscriptions_status 
                ON subscriptions(status);
            """))
            
            print("   ✅ Subscriptions table updated successfully")
            
        except Exception as e:
            print(f"   ⚠️  Warning: {e}")
        
        # 2. Create invoices table
        print("\n📝 Step 2: Creating invoices table...")
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS invoices (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
                    subscription_id INTEGER REFERENCES subscriptions(id) ON DELETE SET NULL,
                    stripe_invoice_id VARCHAR UNIQUE,
                    invoice_number VARCHAR NOT NULL,
                    amount NUMERIC(10, 2) NOT NULL,
                    currency VARCHAR(3) DEFAULT 'USD',
                    status VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    due_date TIMESTAMP,
                    paid_at TIMESTAMP,
                    invoice_pdf VARCHAR,
                    hosted_invoice_url VARCHAR,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Add indexes
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_invoices_company 
                ON invoices(company_id);
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_invoices_stripe 
                ON invoices(stripe_invoice_id);
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_invoices_status 
                ON invoices(status);
            """))
            
            print("   ✅ Invoices table created successfully")
            
        except Exception as e:
            print(f"   ⚠️  Warning: {e}")
        
        # 3. Create payment_methods table
        print("\n📝 Step 3: Creating payment_methods table...")
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS payment_methods (
                    id SERIAL PRIMARY KEY,
                    company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
                    stripe_payment_method_id VARCHAR UNIQUE,
                    type VARCHAR(50) NOT NULL,
                    brand VARCHAR(50),
                    last4 VARCHAR(4),
                    exp_month INTEGER,
                    exp_year INTEGER,
                    is_default BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Add indexes
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_payment_methods_company 
                ON payment_methods(company_id);
            """))
            
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_payment_methods_stripe 
                ON payment_methods(stripe_payment_method_id);
            """))
            
            print("   ✅ Payment methods table created successfully")
            
        except Exception as e:
            print(f"   ⚠️  Warning: {e}")
        
        # 4. Update existing subscriptions to have proper defaults
        print("\n📝 Step 4: Updating existing subscription records...")
        try:
            # Set free plan defaults for existing subscriptions without Stripe data
            await conn.execute(text("""
                UPDATE subscriptions 
                SET 
                    currency = 'USD',
                    amount = 0.00,
                    billing_cycle = 'monthly',
                    payment_method = 'none'
                WHERE stripe_customer_id IS NULL 
                  AND currency IS NULL;
            """))
            
            # Set active status for subscriptions without status
            await conn.execute(text("""
                UPDATE subscriptions 
                SET status = 'active' 
                WHERE status IS NULL OR status = '';
            """))
            
            print("   ✅ Existing records updated")
            
        except Exception as e:
            print(f"   ⚠️  Warning: {e}")
        
        # 5. Add trigger for updated_at timestamps
        print("\n📝 Step 5: Adding timestamp triggers...")
        try:
            # Function for updating timestamps
            await conn.execute(text("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """))
            
            # Trigger for subscriptions
            await conn.execute(text("""
                DROP TRIGGER IF EXISTS update_subscriptions_updated_at ON subscriptions;
                CREATE TRIGGER update_subscriptions_updated_at 
                BEFORE UPDATE ON subscriptions 
                FOR EACH ROW 
                EXECUTE FUNCTION update_updated_at_column();
            """))
            
            # Trigger for invoices
            await conn.execute(text("""
                DROP TRIGGER IF EXISTS update_invoices_updated_at ON invoices;
                CREATE TRIGGER update_invoices_updated_at 
                BEFORE UPDATE ON invoices 
                FOR EACH ROW 
                EXECUTE FUNCTION update_updated_at_column();
            """))
            
            # Trigger for payment_methods
            await conn.execute(text("""
                DROP TRIGGER IF EXISTS update_payment_methods_updated_at ON payment_methods;
                CREATE TRIGGER update_payment_methods_updated_at 
                BEFORE UPDATE ON payment_methods 
                FOR EACH ROW 
                EXECUTE FUNCTION update_updated_at_column();
            """))
            
            print("   ✅ Timestamp triggers added")
            
        except Exception as e:
            print(f"   ⚠️  Warning: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("\nNext steps:")
    print("1. Configure Stripe API keys in .env file")
    print("2. Create Price objects in Stripe Dashboard")
    print("3. Update STRIPE_PRICE_IDS in backend/subscription_config.py")
    print("4. Test webhook endpoint with Stripe CLI")
    print("5. Deploy to Railway and update production environment variables")
    print("\n" + "=" * 60)


async def rollback_migration():
    """Rollback migration (use with caution!)"""
    
    print("⚠️  WARNING: This will remove subscription system tables!")
    confirm = input("Type 'ROLLBACK' to confirm: ")
    
    if confirm != "ROLLBACK":
        print("Rollback canceled")
        return
    
    print("\n🔄 Rolling back migration...")
    
    async with engine.begin() as conn:
        # Drop tables
        await conn.execute(text("DROP TABLE IF EXISTS payment_methods CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS invoices CASCADE;"))
        
        # Remove columns from subscriptions
        await conn.execute(text("""
            ALTER TABLE subscriptions 
            DROP COLUMN IF EXISTS stripe_customer_id,
            DROP COLUMN IF EXISTS stripe_subscription_id,
            DROP COLUMN IF EXISTS stripe_price_id,
            DROP COLUMN IF EXISTS payment_method,
            DROP COLUMN IF EXISTS currency,
            DROP COLUMN IF EXISTS amount,
            DROP COLUMN IF EXISTS billing_cycle,
            DROP COLUMN IF EXISTS current_period_start,
            DROP COLUMN IF EXISTS current_period_end,
            DROP COLUMN IF EXISTS cancel_at,
            DROP COLUMN IF EXISTS canceled_at;
        """))
        
        print("✅ Rollback completed")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration for subscription system")
    parser.add_argument(
        "--rollback",
        action="store_true",
        help="Rollback migration (removes subscription tables)"
    )
    
    args = parser.parse_args()
    
    if args.rollback:
        asyncio.run(rollback_migration())
    else:
        asyncio.run(run_migration())
