from typing import List
from .models import Company, BusinessCard
import asyncio


async def create_company(data: Company) -> Company:
    """Placeholder: create a company record.

    Replace with DB persistence logic.
    """
    await asyncio.sleep(0)  # keep as async placeholder
    return data


async def list_companies() -> List[Company]:
    """Placeholder: list companies."""
    await asyncio.sleep(0)
    return []


async def create_card(data: BusinessCard) -> BusinessCard:
    """Placeholder: create a business card record."""
    await asyncio.sleep(0)
    return data


async def list_cards(company_id: int) -> List[BusinessCard]:
    """Placeholder: list business cards for a company."""
    await asyncio.sleep(0)
    return []
