from app.services.fraud.engine import FraudEngine
from app.services.fraud.rules.high_amount import HighAmountRule
from app.services.fraud.rules.velocity import VelocityRule
from app.services.fraud.rules.location import KeyLocationRule
from app.services.fraud.rules.new_merchant import NewMerchantHighAmountRule
from app.services.fraud.rules.collect_scam import CollectScamRule

# Initialize engine
fraud_engine = FraudEngine()

# Register rules
fraud_engine.register_rule(HighAmountRule())
fraud_engine.register_rule(VelocityRule())
fraud_engine.register_rule(KeyLocationRule())
fraud_engine.register_rule(NewMerchantHighAmountRule())
fraud_engine.register_rule(CollectScamRule())
