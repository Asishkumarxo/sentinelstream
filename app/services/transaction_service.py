from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionList
import uuid
from datetime import datetime

class TransactionService:
    async def process_transaction(self, db: AsyncSession, transaction_data: TransactionCreate) -> TransactionResponse:
        # Create DB model
        db_transaction = Transaction(
            user_id=transaction_data.user_id,
            amount=transaction_data.amount,
            currency=transaction_data.currency,
            merchant=transaction_data.merchant,
            transaction_type=transaction_data.transaction_type,
            category=transaction_data.category,
            status="approved", # Auto-approve for now
            fraud_score=0.0,
            is_fraudulent=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)
        
        return TransactionResponse(
            transaction_id=uuid.UUID(db_transaction.id),
            status=db_transaction.status,
            fraud_score=db_transaction.fraud_score,
            message="Transaction processed successfully",
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
