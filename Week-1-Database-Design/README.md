# Week 1 – Fraud Detection Strategy & ML Design (Member 3)

## Role
Machine Learning & Fraud Logic Engineer

## Objective
Design the fraud detection intelligence layer for SentinelStream,
including rule-based fraud detection, machine learning approach,
risk scoring logic, and system data integration.

## Scope of Work (Week 1)

The following fraud detection design and research components
were completed as part of Week 1:

- Common fraud scenarios in digital payment systems
- Rule-based fraud detection logic
- Machine learning feature planning
- ML approach selection (Isolation Forest)
- Data flow and synchronization with backend and frontend systems
- Risk scoring and fraud decision strategy

## Key Design Decisions

1. Fraud detection uses a **layered approach**:
   - Rule-based checks for explainability
   - ML-based anomaly detection for unknown patterns

2. **Unsupervised learning (Isolation Forest)** is chosen:
   - No dependency on labeled fraud data
   - Suitable for real-time, low-latency systems

3. Fraud decisions are based on a **combined risk score**:
   - Rule-based risk score
   - ML anomaly score

4. Final transaction outcomes:
   - ALLOW
   - FLAG FOR REVIEW
   - BLOCK

## Data Dependencies

### From Backend (Member 1)
- Transaction metadata
- User history and behavioral patterns
- Device fingerprints
- Login attempt logs

### From Frontend (Member 2)
- Device information
- Location data (GPS / IP-based)
- User confirmation signals

## Constraints & Assumptions

- Location data may not always be available
  → IP-based geolocation used as fallback

- New users may lack historical data
  → Conservative fraud rules applied

- Some data is unavailable due to privacy regulations:
  - SIM card data
  - Contact list access
  - Biometric liveness detection

## Folder Structure (Fraud Research)

