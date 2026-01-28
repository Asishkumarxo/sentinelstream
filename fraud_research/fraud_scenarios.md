# Common Fraud Scenarios

This document describes common fraud scenarios observed in
digital payment systems, based on industry research and
India’s UPI fraud landscape.

---

## Scenario 1: High Transaction Amount
**Description:**  
A transaction amount significantly higher than the user’s
historical spending pattern.

**Example:**  
User’s average transaction is ₹2,000, but suddenly sends
₹50,000 to an unknown beneficiary.

**Risk Level:** High  
**Detection Signal:**  
`transaction_amount > (user_avg_amount × 2.5)`

---

## Scenario 2: Transaction Velocity / High Frequency
**Description:**  
Unusually high number of transactions in a short time window,
indicating account compromise or automated fraud.

**Example:**  
20 transactions in 5 minutes to different recipients.

**Risk Level:** High  
**Detection Signal:**  
`txn_count_last_5min > 10 OR txn_count_last_1hour > 30`
---

## Scenario 3: Location Mismatch / Impossible Travel
**Description:**  
Two consecutive transactions from geographically distant locations
in an impossibly short time.

**Example:**  
Transaction in Chennai at 10:00 AM, then Delhi at 10:15 AM.

**Risk Level:** High  
**Detection Signal:**  
`location_distance_km > 500 AND time_since_last_txn < 3600`

---

## Scenario 4: Unusual Time Behavior
**Description:**  
Transactions occurring at times when the user normally does not transact.

**Example:**  
User usually transacts between 9 AM–9 PM, but suddenly transacts at 4 AM.

**Risk Level:** Medium  
**Detection Signal:**  
`time_of_day < 6 AND user_typical_hours = [9,21]`

---

## Scenario 5: New Payee / Unknown Beneficiary
**Description:**  
First-time transaction to a newly added beneficiary with a high amount.

**Example:**  
User sends ₹25,000 to a new UPI ID.

**Risk Level:** Medium  
**Detection Signal:**  
`new_payee == 1 AND transaction_amount > user_avg_amount × 1.5`

---

## Scenario 6: Device / IP Address Change
**Description:**  
Sudden transaction from a new device or IP location.

**Example:**  
User switches from iPhone (Chennai) to Android (Bangladesh IP).

**Risk Level:** Medium  
**Detection Signal:**  
`new_device == 1 OR ip_location_change > 1000`

---

## Scenario 7: Account Takeover (SIM Cloning)
**Description:**  
Multiple failed login attempts followed by a successful transaction.

**Example:**  
10 failed OTP attempts, then a large transaction.

**Risk Level:** High  
**Detection Signal:**  
`failed_login_attempts > 5 AND time_since_login < 300`

---

## Scenario 8: Collect Request Scam
**Description:**  
Incoming collect requests from unknown UPI IDs claiming refunds.

**Example:**  
“Approve refund ₹10,000” from an unknown UPI ID.

**Risk Level:** Medium  
**Detection Signal:**  
`collect_request_from_new_upi == 1`
