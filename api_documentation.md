# SentinelStream API Documentation

## Base URL: http://localhost:8000/api/v1


## Authentication
- API Key in header: `X-API-Key: your-api-key`
- Idempotency Key: `Idempotency-Key: unique-string`

## Endpoints

### 1. POST /transactions
**Create a new transaction**

**Headers:**
- `Idempotency-Key: string` (required)
- `Content-Type: application/json`

**Request Body:**
```json
{
  "user_id": "user_123",
  "amount": 100.50,
  "currency": "USD",
  "transaction_type": "deposit",
  "recipient_id": "user_456",
  "description": "Monthly salary"
}