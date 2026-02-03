from sqlalchemy import Column, String, Float, DateTime, Boolean, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False) # In production consider DECIMAL for money
    currency = Column(String(3), nullable=False)
    merchant = Column(String, nullable=True) # Matches schema
    category = Column(String, nullable=True)
    transaction_type = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, approved, rejected
    
    # Fraud Detection
    fraud_score = Column(Float, default=0.0)
    is_fraudulent = Column(Boolean, default=False)
    
    # Idempotency
    idempotency_key = Column(String, unique=True, index=True, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
