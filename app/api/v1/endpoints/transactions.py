from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction import TransactionCreate, TransactionResponse, TransactionList
from app.services.transaction_service import transaction_service
from app.core.database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db)
):
    return await transaction_service.process_transaction(db, transaction)

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await transaction_service.get_transaction_by_id(db, transaction_id)
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result

@router.get("/users/{user_id}", response_model=TransactionList)
async def get_user_history(
    user_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await transaction_service.get_user_transactions(db, user_id, page, page_size)
