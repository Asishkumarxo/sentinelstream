
# Week 1 – Database Design (Member 2)

## Role
Database & Infrastructure Engineer

## Objective
Design the database schema for SentinelStream and align it with backend APIs.

## Tables Designed
- users
- accounts
- transactions (IMMUTABLE)
- fraud_logs
- audit_logs

## Key Rules
1. Transactions table is INSERT ONLY (no updates/deletes).
2. idempotency_key is UNIQUE to prevent duplicate transactions.
3. fraud_logs and audit_logs are append-only.
4. All primary keys use UUID.

## Redis Usage Plan (Design Only)
- Store idempotency keys temporarily to prevent duplicate transactions.
- Maintain rate limiting counters per user/account.
- Cache frequently accessed user and account data.

## Integration Notes for Backend (Member 1)
- Database column names are designed to match API field names.
- `schema.dbml` should be used as the source of truth for table creation.
- Please suggest any required field changes for API alignment.

## Status
Week 1 completed by Member 2.

Add Week 1 database design documentation (Member 2)
