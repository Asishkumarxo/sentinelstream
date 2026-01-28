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
