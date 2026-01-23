from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    """Transaction type enumeration"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal" 
    TRANSFER = "transfer"

class TransactionBase(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    currency: str = Field("USD", description="Currency code (ISO 4217)")
    transaction_type: TransactionType = Field(..., description="Type of transaction")
    recipient_id: Optional[str] = Field(None, description="ID of recipient (for transfers only)")
    description: Optional[str] = Field(None, description="Optional transaction description")

class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction (POST request)"""
    pass

class TransactionResponse(TransactionBase):
    id: str = Field(..., description="Unique transaction identifier")
    status: str = Field(..., description="Transaction status: pending/completed/failed")
    fraud_score: Optional[float] = Field(None, ge=0, le=1, description="Fraud probability score (0-1)")
    fraud_check_passed: bool = Field(False, description="Whether fraud check passed")
    created_at: datetime = Field(..., description="Timestamp when transaction was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when transaction was last updated")
    
    model_config = {
        "from_attributes": True,  # Changed from orm_mode=True
        "json_schema_extra": {    # Changed from schema_extra
            "example": {
                "id": "txn_7a8b9c0d",
                "user_id": "user_123",
                "amount": 100.50,
                "currency": "USD",
                "transaction_type": "deposit",
                "recipient_id": None,
                "description": "Monthly salary deposit",
                "status": "pending",
                "fraud_score": 0.15,
                "fraud_check_passed": True,
                "created_at": "2024-01-23T10:30:00Z",
                "updated_at": "2024-01-23T10:31:00Z"
            }
        }
    }

class TransactionList(BaseModel):
    transactions: list[TransactionResponse] = Field(..., description="List of transactions")
    total: int = Field(..., description="Total number of transactions")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")

# ========== ERROR SCHEMAS ==========

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")

class DuplicateErrorResponse(ErrorResponse):
    idempotency_key: Optional[str] = Field(None, description="The duplicate idempotency key")

class RateLimitErrorResponse(ErrorResponse):
    retry_after: Optional[int] = Field(None, description="Seconds to wait before retrying")