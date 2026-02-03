from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

class FraudRule(ABC):
    """
    Abstract base class for fraud detection rules.
    """
    
    @property
    @abstractmethod
    def rule_id(self) -> str:
        """Unique identifier for the rule."""
        pass
        
    @property
    @abstractmethod
    def rule_name(self) -> str:
        """Human readable name for the rule."""
        pass
        
    @property
    @abstractmethod
    def risk_score(self) -> float:
        """The risk score contributing to the total fraud score if the rule is triggered."""
        pass

    @abstractmethod
    async def evaluate(self, transaction: TransactionCreate, history: List[Transaction]) -> bool:
        """
        Evaluate the transaction against the rule.
        
        Args:
            transaction: The transaction being processed (schema).
            history: List of past transactions for the user (models).
            
        Returns:
            bool: True if fraud is detected (rule triggered), False otherwise.
        """
        pass
