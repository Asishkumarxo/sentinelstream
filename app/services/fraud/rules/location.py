from typing import List
from datetime import datetime
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.fraud.rules.base import FraudRule

class KeyLocationRule(FraudRule):
    """
    Combines Rule 3 (Impossible Travel) and Rule 5 (Device/IP Change).
    Since we don't have a real GeoIP DB, we simulate distance based on IP string difference
    or just trigger on IP change for now.
    """
    @property
    def rule_id(self) -> str:
        return "rule_003_005_location"
        
    @property
    def rule_name(self) -> str:
        return "Location Anomaly"
        
    @property
    def risk_score(self) -> float:
        # Variable score? Base class returns a fixed float however.
        # We can return the max score if both apply, or sum them.
        # For simplicity, if Impossible Travel (worst case), we return 45.
        # If just IP change, we might want lower, but this class structure restricts to single score.
        # So we'll implement checking for Impossible Travel primarily (higher risk).
        return 45.0

    async def evaluate(self, transaction: TransactionCreate, history: List[Transaction]) -> bool:
        if not history:
            return False
            
        if not transaction.ip_address:
            return False
            
        last_txn = history[0] # Assuming history is sorted desc by created_at (we ensure this in service)
        
        # Check if IP changed
        if last_txn.ip_address and last_txn.ip_address != transaction.ip_address:
            # IP Changed.
            
            # Check time difference
            time_diff = datetime.utcnow() - last_txn.created_at
            
            # If transaction happened very quickly from different IP (< 1 hour)
            # We treat this as "Impossible Travel" equivalent for this mock
            if time_diff.total_seconds() < 3600:
                return True
                
        return False
