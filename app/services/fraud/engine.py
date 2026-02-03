from typing import List, Dict, Any
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.fraud.rules.base import FraudRule

class FraudEngine:
    def __init__(self):
        self.rules: List[FraudRule] = []
        
    def register_rule(self, rule: FraudRule):
        """Register a new fraud rule."""
        self.rules.append(rule)
        
    async def evaluate_transaction(self, transaction: TransactionCreate, history: List[Transaction]) -> Dict[str, Any]:
        """
        Evaluate a transaction against all registered rules.
        
        Returns:
            Dict containing:
            - total_score: float
            - is_fraudulent: bool
            - triggered_rules: List[str] (names of triggered rules)
        """
        total_score = 0.0
        triggered_rules = []
        
        for rule in self.rules:
            try:
                # Some rules might need async I/O in the future (e.g., redis check)
                # We awaited evaluate in the base class, so we await here.
                is_triggered = await rule.evaluate(transaction, history)
                
                if is_triggered:
                    total_score += rule.risk_score
                    triggered_rules.append(rule.rule_name)
                    
            except Exception as e:
                # Log error but don't fail the entire process
                print(f"Error evaluating rule {rule.rule_name}: {e}")
                
        # Determine if fraudulent based on threshold
        # Threshold could be configurable. Using 70.0 as per Week 3 goals/docs if applicable, 
        # or defaults. Let's use 50.0 as a conservative default or read from settings.
        # Looking at fraud_rules.md from previous context -> >= 70 is High Risk (Block).
        
        is_fraudulent = total_score >= 70.0
        
        return {
            "total_score": total_score,
            "is_fraudulent": is_fraudulent,
            "triggered_rules": triggered_rules
        }
