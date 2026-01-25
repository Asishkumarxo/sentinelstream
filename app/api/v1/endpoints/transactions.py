from fastapi import APIRouter, HTTPException, Header, Query, status, Request
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
import random
import json
from app.schemas.transaction import (
    TransactionCreate, 
    TransactionResponse,
    TransactionList,
    ErrorResponse,
    DuplicateErrorResponse,
    RateLimitErrorResponse
)

router = APIRouter()

# DEBUG ROUTE - Add this
@router.post("/debug-test")
async def debug_test(request: Request):
    """
    Debug endpoint to see raw request data
    """
    try:
        # Get raw body
        body = await request.body()
        body_str = body.decode('utf-8')
        
        # Try to parse
        parsed = json.loads(body_str)
        
        return {
            "raw_body": body_str,
            "parsed": parsed,
            "transaction_type_value": parsed.get("transaction_type"),
            "transaction_type_type": type(parsed.get("transaction_type")).__name__ if parsed.get("transaction_type") else "None"
        }
    except Exception as e:
        return {"error": str(e), "raw_body": body_str if 'body_str' in locals() else "N/A"}

# POST /transactions
@router.post("/test-simple")
async def test_simple(request: Request):
    """Simple test endpoint that accepts any JSON"""
    try:
        body = await request.json()
        return {
            "success": True,
            "received": body,
            "message": "API is working!"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "JSON parsing failed"
        }
@router.post(
    "/", 
    response_model=TransactionResponse,
    responses={
        409: {"model": DuplicateErrorResponse, "description": "Duplicate Request"},
        429: {"model": RateLimitErrorResponse, "description": "Rate Limit Exceeded"}
    }
)
async def create_transaction(
    request: Request,
    transaction: TransactionCreate,
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    """
    Create a new transaction.
    
    ## Transaction Types:
    - **deposit**: Add funds to account
    - **withdrawal**: Remove funds from account  
    - **transfer**: Move funds between accounts
    
    ## Headers:
    - `Idempotency-Key`: Unique string to prevent duplicate processing
    
    ## Request Validation:
    - Amount must be positive
    - Currency must be valid ISO code
    - User must exist
    
    ## Process Flow:
    1. Validate request
    2. Check for duplicates (idempotency)
    3. Fraud detection check
    4. Store in database
    5. Return transaction details
    """
    
    # Clean idempotency key (remove quotes if present)
    clean_idempotency_key = None
    if idempotency_key:
        clean_idempotency_key = idempotency_key.strip('"\'')
    
    # Check for duplicate (simulated - will use Redis later)
    if clean_idempotency_key == "duplicate_key_example":
        error_response = DuplicateErrorResponse(
            error="Duplicate request detected",
            details="This idempotency key was already processed",
            idempotency_key=clean_idempotency_key
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=error_response.dict(exclude_none=True)
        )
    
    # Rate limiting check (simulated) - 1 in 10 requests get rate limited
    if random.randint(1, 10) == 1:
        error_response = RateLimitErrorResponse(
            error="Rate limit exceeded",
            details="Too many requests, please try again later",
            retry_after=60
        )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content=error_response.dict(exclude_none=True)
        )
    
    # Normal successful response
    return TransactionResponse(
        id=f"txn_{int(datetime.now().timestamp())}",
        user_id=transaction.user_id,
        amount=transaction.amount,
        currency=transaction.currency,
        transaction_type=transaction.transaction_type,
        recipient_id=transaction.recipient_id,
        description=transaction.description,
        status="pending",
        fraud_score=0.15,
        fraud_check_passed=True,
        created_at=datetime.now()
    )

# GET /transactions/{transaction_id}
@router.get(
    "/{transaction_id}", 
    response_model=TransactionResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Transaction not found"}
    }
)
async def get_transaction(
    request: Request,
    transaction_id: str
):
    """
    Get transaction details by ID.
    
    ## Parameters:
    - **transaction_id**: Unique identifier of the transaction
    
    ## Returns:
    - Complete transaction details including status and fraud check results
    """
    # Simulate transaction not found
    if transaction_id == "not_found":
        error_response = ErrorResponse(
            error="Transaction not found",
            details=f"Transaction ID {transaction_id} does not exist"
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=error_response.dict(exclude_none=True)
        )
    
    return TransactionResponse(
        id=transaction_id,
        user_id="user_123",
        amount=100.50,
        currency="USD",
        transaction_type="deposit",
        recipient_id=None,
        description="Sample transaction",
        status="completed",
        fraud_score=0.15,
        fraud_check_passed=True,
        created_at=datetime.now()
    )

# GET /users/{user_id}/transactions
@router.get("/users/{user_id}/transactions", response_model=TransactionList)
async def get_user_transactions(
    user_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """
    Get transaction history for a specific user.
    
    ## Parameters:
    - **user_id**: Unique identifier of the user
    - **page**: Page number for pagination (default: 1)
    - **page_size**: Number of items per page (default: 10, max: 100)
    
    ## Returns:
    - Paginated list of user's transactions
    """
    return TransactionList(
        transactions=[],
        total=0,
        page=page,
        page_size=page_size
    )