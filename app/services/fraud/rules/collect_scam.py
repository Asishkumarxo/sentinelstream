from typing import List
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.fraud.rules.base import FraudRule

class CollectScamRule(FraudRule):
    @property
    def rule_id(self) -> str:
        return "rule_007_collect_scam"
        
    @property
    def rule_name(self) -> str:
        return "Collect Request Scam"
        
    @property
    def risk_score(self) -> float:
        return 15.0

    async def evaluate(self, transaction: TransactionCreate, history: List[Transaction]) -> bool:
        """
        Check if transaction is a 'collect' request from a new entity.
        """
        if transaction.transaction_type != "collect":
            return False
            
        if not history:
            return False
            
        # Check if we have interacted with this merchant/requester before
        past_merchants = {t.merchant for t in history}
        
        if transaction.merchant not in past_merchants:
            # Collect request from a new person/merchant -> Suspicious
            return True
            
        return False
