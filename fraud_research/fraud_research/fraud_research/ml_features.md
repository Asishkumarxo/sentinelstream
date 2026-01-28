# Machine Learning Feature Definitions

This document lists the features used for fraud detection,
derived from transaction data, user behavior, device signals,
and historical patterns.

These features will be used as inputs to the anomaly detection
model (Isolation Forest).

---

## Transaction-Level Features

| Feature Name        | Data Type   | Source       | Description |
|--------------------|-------------|--------------|-------------|
| transaction_amount | Float       | Backend DB   | Amount of the transaction in INR |
| transaction_type   | Categorical | Backend DB   | Type of transaction (UPI, card, transfer) |
| merchant_category  | Categorical | Backend DB   | Category of merchant involved |
| is_new_payee       | Boolean     | Calculated   | Whether the beneficiary is new |
| time_of_day        | Integer     | Calculated   | Hour of transaction (0–23) |

---

## User Behavior Features

| Feature Name              | Data Type | Source      | Description |
|---------------------------|-----------|-------------|-------------|
| avg_transaction_amount    | Float     | Calculated  | User’s historical average spend |
| txn_count_last_5min       | Integer   | Calculated  | Transactions in last 5 minutes |
| txn_count_last_1hour      | Integer   | Calculated  | Transactions in last 1 hour |
| failed_login_attempts     | Integer   | Auth Logs   | Failed login or OTP attempts |

---

## Device & Network Features

| Feature Name            | Data Type   | Source     | Description |
|-------------------------|-------------|------------|-------------|
| new_device_flag         | Boolean     | Frontend   | Indicates new device usage |
| ip_location_change_km   | Float       | Calculated | Distance from last known location |
| device_os               | Categorical | Frontend   | Operating system of device |

---

## Label / Target (Not Used for Training)

This system uses **unsupervised learning**, so fraud labels
are not required during model training. Labels are used only
for evaluation and rule tuning.
