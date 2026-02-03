# 🛡️ Week 3: Fraud Detection Algorithms - ✅ COMPLETED

**Team Member**: Fraud Detection Engineer  
**Duration**: 1 Week  
**Status**: ✅ Implementation Complete & Verified

## 📋 What We Built

### 1. Fraud Detection Engine
We implemented a modular **Rule-Based Fraud Engine** (`app.services.fraud`) that evaluates every transaction in real-time.

- **Architecture**:
    - `FraudEngine`: Aggregates scores from multiple logic rules.
    - `FraudRule`: Abstract base class for defining new fraud logic easily.

### 2. Activated Fraud Rules
The following rules are now active:

| Rule ID | Name | Condition | Risk Score |
|:---|:---|:---|:---|
| `rule_001` | **High Amount** | Amount > $10k OR > 2.5x User Avg | `+40` |
| `rule_002` | **Velocity** | > 10 transactions in 1 hour | `+35` |
| `rule_003` | **Location Anomaly** | IP Change & Time < 1h (Simulated Impossible Travel) | `+45` |
| `rule_004` | **New User/Merchant** | New Payee & High Amount | `+25` |
| `rule_007` | **Collect Scam** | Collect request from new entity | `+15` |

### 3. Service Integration
- **Transaction Service**: Now calls `FraudEngine.evaluate_transaction()` before saving.
- **Outcomes**:
    - **Score ≥ 70**: Status `rejected` ⛔
    - **Score ≥ 40**: Status `flagged` ⚠️
    - **Score < 40**: Status `approved` ✅

### 4. Database Updates
- Added `ip_address` and `user_agent` to `transactions` table to support location-based rules.
- Created Alembic migration `1234abcd5678_add_ip_and_user_agent.py`.

## 🧪 Verification
- **Unit Tests**: `tests/test_fraud_rules.py` verifies all rule logic (High amount, velocity, location, etc.).
- **Manual Verification**: Verified via `pytest` passing all checks.

---

## 🚀 How to Run

1. **Install Dependencies** (if not already installed)
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Migrations**
   ```bash
   alembic upgrade head
   ```

3. **Run Tests**
   ```bash
   python -m pytest tests/test_fraud_rules.py
   ```
