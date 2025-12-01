# PostgreSQL HA Notes

High-level notes and patterns for designing PostgreSQL HA.

## Patterns

- Primary + async replica (same DC)
- Primary + sync replica (same DC) + async replica (DR)
- Using repmgr / Patroni / other orchestrators

## Things to watch

- Replication lag (see `pg_lag_check.py`)
- Slot retention & disk usage (see `pg_replication_slot_usage.sql`)
- Promotion/failover procedures:
  - How to promote
  - How apps re-point
  - How to reintroduce the old primary as a replica
