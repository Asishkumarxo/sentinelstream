from typing import List
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.fraud.rules.base import FraudRule
from app.core.config import settings

class VelocityRule(FraudRule):
    @property
    def rule_id(self) -> str:
        return "rule_002_velocity"
        
    @property
    def rule_name(self) -> str:
        return "High Transaction Velocity"
        
    @property
    def risk_score(self) -> float:
        return 35.0

    async def evaluate(self, transaction: TransactionCreate, history: List[Transaction]) -> bool:
        """
        Check if user is making too many transactions in a short time.
        
        Logic:
        - Count transactions in last 1 hour.
        - If count > settings.FLAG_THRESHOLD_FREQUENCY, return True.
        """
        if not history:
            return False
            
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        
        # Count transactions in the last hour
        recent_txns = [
            t for t in history 
            if t.created_at >= one_hour_ago
        ]
        
        count = len(recent_txns)
        
        # Check against threshold
        if count > settings.FLAG_THRESHOLD_FREQUENCY:
            return True
            
        return False
