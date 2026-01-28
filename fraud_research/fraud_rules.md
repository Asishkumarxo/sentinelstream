# Fraud Rule Definitions

This document defines the rule-based fraud detection logic
used in SentinelStream. These rules are configurable and
designed to provide explainable fraud decisions.

Each rule contributes a risk score that is later combined
with the machine learning anomaly score.

---

## Rule 1: High Transaction Amount
**Condition:**  
IF `transaction_amount > (user_avg_amount × 2.5)`

**Risk Score Added:** +40  

**Reason:**  
A sudden high-value transaction may indicate account takeover
or unauthorized access.

---

## Rule 2: High Transaction Velocity
**Condition:**  
IF `txn_count_last_5min > 10` OR `txn_count_last_1hour > 30`

**Risk Score Added:** +35  

**Reason:**  
Multiple rapid transactions are common in automated fraud
and scripted attacks.

---

## Rule 3: Impossible Travel / Location Mismatch
**Condition:**  
IF `location_distance_km > 500` AND `time_since_last_txn < 1 hour`

**Risk Score Added:** +45  

**Reason:**  
It is physically impossible for a user to travel such
distances in a short time.

---

## Rule 4: New Payee with High Amount
**Condition:**  
IF `is_new_payee = TRUE` AND `transaction_amount > user_avg_amount × 1.5`

**Risk Score Added:** +25  

**Reason:**  
Fraudsters often add a new beneficiary before attempting
large fund transfers.

---

## Rule 5: Device or IP Change
**Condition:**  
IF `new_device_flag = TRUE` OR `ip_location_change_km > 1000`

**Risk Score Added:** +20  

**Reason:**  
A sudden change in device or IP location can indicate
suspicious login behavior.

---

## Rule 6: Multiple Failed Login Attempts
**Condition:**  
IF `failed_login_attempts > 5`

**Risk Score Added:** +30  

**Reason:**  
Repeated failed logins may indicate brute-force or SIM-swap
attempts.

---

## Rule 7: Collect Request Scam
**Condition:**  
IF `collect_request_from_new_upi = TRUE`

**Risk Score Added:** +15  

**Reason:**  
Fake refund and collect-request scams are common in UPI
payment frauds.

---

## Rule Evaluation Outcome

- **Total Rule Score ≥ 70** → High Risk (Block Transaction)  
- **Total Rule Score 40–69** → Medium Risk (Flag for Review)  
- **Total Rule Score < 40** → Low Risk (Allow Transaction)
