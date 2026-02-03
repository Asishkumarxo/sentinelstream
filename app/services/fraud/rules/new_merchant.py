from typing import List
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.fraud.rules.base import FraudRule

class NewMerchantHighAmountRule(FraudRule):
    @property
    def rule_id(self) -> str:
        return "rule_004_new_merchant_high_amount"
        
    @property
    def rule_name(self) -> str:
        return "New Merchant High Amount"
        
    @property
    def risk_score(self) -> float:
        return 25.0

    async def evaluate(self, transaction: TransactionCreate, history: List[Transaction]) -> bool:
        """
        Check if it's a new merchant AND amount is higher than usual.
        
        Logic:
        1. Check if merchant exists in user history.
        2. If New Merchant AND Amount > 1.5 * User Average, return True.
        """
        if not history:
            # No history means everything is new, but we can't calculate average.
            # We could be strict or lenient. Let's be lenient for first transaction.
            return False
            
        # Check if merchant is new
        past_merchants = {t.merchant for t in history}
        is_new_merchant = transaction.merchant not in past_merchants
        
        if not is_new_merchant:
            return False
            
        # Calculate average amount
        total_past_amount = sum(t.amount for t in history)
        avg_amount = total_past_amount / len(history)
        
        # Check amount condition (> 1.5x average)
        if transaction.amount > (avg_amount * 1.5):
            return True
            
        return False
