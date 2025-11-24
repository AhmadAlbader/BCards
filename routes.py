from fastapi import APIRouter, HTTPException
from typing import List

from .models import Company, BusinessCard
from . import services

router = APIRouter(prefix="/digital-cards", tags=["digital-cards"])


@router.post("/companies", response_model=Company)
async def create_company(company: Company):
    created = await services.create_company(company)
    return created


@router.get("/companies", response_model=List[Company])
async def get_companies():
    return await services.list_companies()


@router.post("/companies/{company_id}/cards", response_model=BusinessCard)
async def create_business_card(company_id: int, card: BusinessCard):
    if card.company_id != company_id:
        raise HTTPException(status_code=400, detail="company_id mismatch")
    created = await services.create_card(card)
    return created


@router.get("/companies/{company_id}/cards", response_model=List[BusinessCard])
async def get_business_cards(company_id: int):
    return await services.list_cards(company_id)
