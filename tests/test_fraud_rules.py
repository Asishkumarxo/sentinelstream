import pytest
from datetime import datetime, timedelta
from app.services.fraud.rules.high_amount import HighAmountRule
from app.services.fraud.rules.velocity import VelocityRule
from app.services.fraud.rules.location import KeyLocationRule
from app.services.fraud.rules.new_merchant import NewMerchantHighAmountRule
from app.services.fraud.rules.collect_scam import CollectScamRule
from app.schemas.transaction import TransactionCreate
from app.models.transaction import Transaction
from app.core.config import settings

@pytest.fixture
def mock_history():
    return [
        Transaction(
            amount=100.0,
            merchant="Amazon",
            created_at=datetime.utcnow() - timedelta(minutes=30),
            ip_address="127.0.0.1"
        ),
        Transaction(
            amount=200.0,
            merchant="Netflix",
            created_at=datetime.utcnow() - timedelta(days=1),
            ip_address="127.0.0.1"
        )
    ]

@pytest.mark.asyncio
async def test_high_amount_rule(mock_history):
    rule = HighAmountRule()
    
    # normal amount
    tx_normal = TransactionCreate(
        user_id="user1", amount=150.0, currency="USD", merchant="Test", transaction_type="purchase"
    )
    assert await rule.evaluate(tx_normal, mock_history) == False
    
    # global threshold check
    tx_huge = TransactionCreate(
        user_id="user1", amount=settings.FLAG_THRESHOLD_AMOUNT + 1, currency="USD", merchant="Test", transaction_type="purchase"
    )
    assert await rule.evaluate(tx_huge, mock_history) == True
    
    # user average check (avg is 150. 2.5x is 375)
    tx_high_avg = TransactionCreate(
        user_id="user1", amount=400.0, currency="USD", merchant="Test", transaction_type="purchase"
    )
    assert await rule.evaluate(tx_high_avg, mock_history) == True

@pytest.mark.asyncio
async def test_velocity_rule():
    rule = VelocityRule()
    
    # Create history with 11 transactions in last hour
    recent_history = [
        Transaction(created_at=datetime.utcnow() - timedelta(minutes=i))
        for i in range(11)
    ]
    
    tx = TransactionCreate(user_id="u1", amount=10, currency="USD", merchant="m", transaction_type="purchase")
    
    # Threshold is 10
    assert await rule.evaluate(tx, recent_history) == True
    
    # Only 5 txns
    assert await rule.evaluate(tx, recent_history[:5]) == False

@pytest.mark.asyncio
async def test_location_rule():
    rule = KeyLocationRule()
    
    # Lasttxn was 30 mins ago at 127.0.0.1
    history = [Transaction(created_at=datetime.utcnow() - timedelta(minutes=30), ip_address="127.0.0.1")]
    
    # Same IP
    tx_same = TransactionCreate(user_id="u", amount=10, currency="USD", merchant="m", ip_address="127.0.0.1", transaction_type="purchase")
    assert await rule.evaluate(tx_same, history) == False
    
    # Diff IP, fast travel
    tx_diff = TransactionCreate(user_id="u", amount=10, currency="USD", merchant="m", ip_address="192.168.1.1", transaction_type="purchase")
    assert await rule.evaluate(tx_diff, history) == True
    
    # Diff IP, slow travel (>1h)
    history_old = [Transaction(created_at=datetime.utcnow() - timedelta(hours=2), ip_address="127.0.0.1")]
    assert await rule.evaluate(tx_diff, history_old) == False

@pytest.mark.asyncio
async def test_new_merchant_high_amount(mock_history):
    # History merchants: Amazon, Netflix. Avg amount: 150.
    rule = NewMerchantHighAmountRule()
    
    # Existing merchant, high amount -> False (only new merchant triggers)
    tx_amazon = TransactionCreate(user_id="u", amount=1000.0, currency="USD", merchant="Amazon", transaction_type="purchase")
    assert await rule.evaluate(tx_amazon, mock_history) == False
    
    # New Merchant, normal amount -> False
    tx_new = TransactionCreate(user_id="u", amount=100.0, currency="USD", merchant="NewStore", transaction_type="purchase")
    assert await rule.evaluate(tx_new, mock_history) == False
    
    # New Merchant, High Amount (> 1.5 * 150 = 225)
    tx_suspicious = TransactionCreate(user_id="u", amount=250.0, currency="USD", merchant="NewStore", transaction_type="purchase")
    assert await rule.evaluate(tx_suspicious, mock_history) == True

@pytest.mark.asyncio
async def test_collect_scam_rule(mock_history):
    rule = CollectScamRule()
    
    # Normal purchase
    tx_purchase = TransactionCreate(user_id="u", amount=10, currency="USD", merchant="any", transaction_type="purchase")
    assert await rule.evaluate(tx_purchase, mock_history) == False
    
    # Collect from known merchant -> False
    tx_collect_known = TransactionCreate(user_id="u", amount=10, currency="USD", merchant="Amazon", transaction_type="collect")
    assert await rule.evaluate(tx_collect_known, mock_history) == False
    
    # Collect from NEW merchant -> True
    tx_collect_new = TransactionCreate(user_id="u", amount=10, currency="USD", merchant="Stranger", transaction_type="collect")
    assert await rule.evaluate(tx_collect_new, mock_history) == True
