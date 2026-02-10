import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_transaction(async_client):
    payload = {
        "user_id": "test_user_1",
        "amount": 100.0,
        "currency": "USD",
        "merchant": "Amazon",
        "transaction_type": "purchase"
    }
    response = await async_client.post("/api/v1/transactions/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert "transaction_id" in data
    assert data["status"] in ["approved", "rejected", "flagged"]

@pytest.mark.asyncio
async def test_create_transaction_high_risk(async_client):
    # Depending on rules, this might be flagged or rejected
    payload = {
        "user_id": "test_user_2",
        "amount": 1000000.0, # Very high amount
        "currency": "USD",
        "merchant": "Unknown",
        "transaction_type": "purchase"
    }
    response = await async_client.post("/api/v1/transactions/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["status"] == "rejected" or data["fraud_score"] >= 70

@pytest.mark.asyncio
async def test_invalid_transaction(async_client):
    payload = {
        "user_id": "test_user_3",
        # Missing amount
        "currency": "USD",
        "merchant": "Amazon"
    }
    response = await async_client.post("/api/v1/transactions/", json=payload)
    assert response.status_code == 422
