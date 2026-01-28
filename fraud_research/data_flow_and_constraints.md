# Data Sync with Members 1 & 2

This document explains how data flows between the backend,
frontend, and the ML fraud detection engine, along with
data availability, reliability, and system constraints.

---

## Data Flow Overview

- **Member 1 (Backend):**
  - User Database
  - Transaction Database
  - Device Fingerprints
  - Login Logs

- **Member 2 (Frontend):**
  - User location data
  - Device information
  - User behavior signals

- **Member 3 (ML Engine & Fraud Logic):**
  - Receives data via REST API / Event Stream
  - Applies rule-based checks
  - Computes ML anomaly score
  - Sends final decision (Allow / Review / Block) back to frontend

---

## Data Available from Member 1 (Backend / Database)

| Data Field | Type | Availability | Reliability | Notes |
|-----------|------|--------------|-------------|------|
| user_id | String | Real-time | Very High | Unique user identifier |
| transaction_id | String | Real-time | Very High | Unique transaction ID |
| timestamp | DateTime | Real-time | Very High | Server timestamp (UTC) |
| transaction_amount | Float | Real-time | Very High | INR amount |
| to_upi / to_account | String | Real-time | Very High | Beneficiary identifier |
| from_account | String | Real-time | Very High | Payer account |
| txn_status | String | Real-time | Very High | Success / Failed / Pending |
| device_id | String | Real-time | High | Device fingerprint hash |
| ip_address | String | Real-time | High | Source IP address |
| user_avg_amount | Float | Batch (hourly) | High | Avg transaction value (30 days) |
| txn_count_last_Xmin | Int | Real-time | High | Transaction velocity |
| failed_login_attempts | Int | Real-time | High | From login logs |
| account_age_days | Int | Static | Very High | Days since account creation |
| beneficiary_list | List | Batch (daily) | High | User’s known beneficiaries |
| typical_txn_hours | List | Batch (daily) | Medium | Normal transaction hours |

---

## Data Available from Member 2 (Frontend / App)

| Data Field | Type | Availability | Reliability | Notes |
|-----------|------|--------------|-------------|------|
| location_city | String | Real-time | Medium | Requires location permission |
| location_coordinates | Tuple (lat, lon) | Real-time | Medium | GPS may fail indoors |
| device_type | String | Real-time | High | Android / iOS / Web |
| device_model | String | Real-time | High | Mobile model |
| app_version | String | Real-time | High | Application version |
| os_version | String | Real-time | High | OS version |
| screen_size | String | Real-time | High | Screen dimensions |
| network_type | String | Real-time | High | WiFi / 4G / 5G |
| user_confirmation | Boolean | Real-time | Very High | User explicitly approved transaction |
| biometric_auth | Boolean | Real-time | Very High | Fingerprint / FaceID |

---

## Confirmed Data Availability

- Real-time transaction metadata
- Device and network information
- Historical transaction patterns (last 30 days)
- IP-based geolocation
- Login attempt logs

---

## Data Constraints and Assumptions

- GPS location may not always be available  
  → Fallback to IP-based geolocation

- New users may not have sufficient history  
  → Apply conservative default rules

- Some data cannot be accessed due to privacy:
  - SIM card information
  - Contact list analysis
  - Biometric liveness detection

---

## Data Format Agreement (JSON Schema)

All data exchanged between Member 1, Member 2, and Member 3
follows a standardized JSON structure:

```json
{
  "user_id": "usr_123456",
  "transaction_id": "txn_987654",
  "timestamp": "2026-01-25T14:30:45Z",
  "transaction_amount": 5000.00,
  "to_upi": "user@bankname",
  "device_id": "device_abc123xyz",
  "ip_address": "203.0.113.45",
  "location_city": "Chennai",
  "features": {
    "amount_ratio": 2.0,
    "txn_count_last_5min": 3,
    "time_of_day": 14,
    "is_weekend": 0,
    "location_distance_km": 0,
    "new_payee": 1,
    "new_device": 0
  },
  "rule_score": 40,
  "ml_anomaly_score": 0.45,
  "final_risk_score": 40,
  "decision": "ALLOW"
}
