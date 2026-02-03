from typing import List
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.fraud.rules.base import FraudRule
from app.core.config import settings

class HighAmountRule(FraudRule):
    @property
    def rule_id(self) -> str:
        return "rule_001_high_amount"
        
    @property
    def rule_name(self) -> str:
        return "High Transaction Amount"
        
    @property
    def risk_score(self) -> float:
        return 40.0

    async def evaluate(self, transaction: TransactionCreate, history: List[Transaction]) -> bool:
        """
        Check if transaction amount is unusually high.
        
        Logic:
        1. If amount > Global Threshold (settings.FLAG_THRESHOLD_AMOUNT), return True.
        2. If user has history, check if amount > 2.5 * average of past transactions.
        """
        # Global threshold check
        if transaction.amount > settings.FLAG_THRESHOLD_AMOUNT:
            return True
            
        # User history average check
        if history:
            total_past_amount = sum(t.amount for t in history)
            avg_amount = total_past_amount / len(history)
            
            # If current amount is > 2.5x the average
            if transaction.amount > (avg_amount * 2.5):
                return True
                
        return False
