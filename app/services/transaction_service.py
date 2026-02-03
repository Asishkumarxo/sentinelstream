from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionList
import uuid
from datetime import datetime

class TransactionService:
    async def process_transaction(self, db: AsyncSession, transaction_data: TransactionCreate) -> TransactionResponse:
        from app.services.fraud import fraud_engine
        
        # Fetch recent user history for fraud detection context
        # Fetching last 100 transactions to balance performance and rule accuracy
        stmt = select(Transaction).where(Transaction.user_id == transaction_data.user_id).order_by(desc(Transaction.created_at)).limit(100)
        result = await db.execute(stmt)
        history = result.scalars().all()
        
        # Evaluate Fraud
        fraud_result = await fraud_engine.evaluate_transaction(transaction_data, history)
        
        fraud_score = fraud_result["total_score"]
        is_fraudulent = fraud_result["is_fraudulent"]
        triggered_rules = fraud_result["triggered_rules"]
        
        # Determine Status
        status = "approved"
        if fraud_score >= 70.0:
            status = "rejected"
        elif fraud_score >= 40.0:
            status = "flagged"
            
        message = "Transaction processed successfully"
        if status == "rejected":
            message = f"Transaction rejected due to high risk: {', '.join(triggered_rules)}"
        elif status == "flagged":
            message = f"Transaction flagged for review: {', '.join(triggered_rules)}"
            
        # Create DB model
        db_transaction = Transaction(
            user_id=transaction_data.user_id,
            amount=transaction_data.amount,
            currency=transaction_data.currency,
            merchant=transaction_data.merchant,
            transaction_type=transaction_data.transaction_type,
            category=transaction_data.category,
            status=status,
            fraud_score=fraud_score,
            is_fraudulent=is_fraudulent,
            ip_address=transaction_data.ip_address,
            user_agent=transaction_data.user_agent,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)
        
        return TransactionResponse(
            transaction_id=uuid.UUID(db_transaction.id),
            status=db_transaction.status,
            amount=db_transaction.amount,
            currency=db_transaction.currency,
            merchant=db_transaction.merchant,
            fraud_score=db_transaction.fraud_score,
            message=message,
            timestamp=db_transaction.created_at
        )

    async def get_transaction_by_id(self, db: AsyncSession, transaction_id: str) -> TransactionResponse | None:
        result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalars().first()
        
        if not transaction:
            return None
            
        return TransactionResponse(
            transaction_id=uuid.UUID(transaction.id),
            status=transaction.status,
            amount=transaction.amount,
            currency=transaction.currency,
            merchant=transaction.merchant,
            fraud_score=transaction.fraud_score,
            message="Retrieved successfully",
            timestamp=transaction.created_at
        )

    async def get_user_transactions(self, db: AsyncSession, user_id: str, page: int, page_size: int) -> TransactionList:
        offset = (page - 1) * page_size
        
        # Get total count (simplification for now, usually separate query)
        # For simplicity in async, doing two queries
        stmt = select(Transaction).where(Transaction.user_id == user_id).order_by(desc(Transaction.created_at))
        
        # This is not efficient for large tables, but okay for Week 2 start
        result = await db.execute(stmt)
        all_rows = result.scalars().all()
        total = len(all_rows)
        
        # Slice for pagination in memory (since we fetched all to count) 
        # TODO: Optimize with count(*) query
        paginated_rows = all_rows[offset : offset + page_size]
        
        transactions = [
            TransactionResponse(
                transaction_id=uuid.UUID(t.id),
                status=t.status,
                amount=t.amount,
                currency=t.currency,
                merchant=t.merchant,
                fraud_score=t.fraud_score,
                message="History item",
                timestamp=t.created_at
            ) for t in paginated_rows
        ]
        
        return TransactionList(
            transactions=transactions,
            total=total,
            page=page,
            page_size=page_size
        )

# Export class, not instance, to allow dependency injection of service if needed, 
# or use a singleton but pass DB session.
transaction_service = TransactionService()
