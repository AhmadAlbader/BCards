#!/usr/bin/env python3
"""Quick test of list employees with Bearer token"""
import httpx
import json

async def test():
    async with httpx.AsyncClient() as client:
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMGZmZmU1Yy05ODZlLTRjMDItODk2Yy0xN2U4MGE1YmM2MjYiLCJjb21wYW55X2lkIjoiOWY4MzFiNDUtMGY0Yi00ZDQ2LWIxYzctOWU3MTRkNjkzNjkyIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY0NTE3ODE2fQ.q2aiAdlJY9zB6QNhmuAcmlKwprkmV2Lnldto59ASFLk"
        company_id = "9f831b45-0f4b-4d46-b1c7-9e714d693692"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.get(
            f"http://localhost:8000/api/company/{company_id}/employees",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content length: {len(response.content)}")
        print(f"Text: {response.text[:500]}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
