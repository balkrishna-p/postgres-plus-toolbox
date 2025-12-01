# Postgres Plus Toolbox

Production-ready tools, queries, and notes for **PostgreSQL** (primary focus), with supporting utilities for **MySQL** and **MongoDB**.

> Built and maintained by [Balkrishna Pandey](https://github.com/balkrishna-p) – DBA & infrastructure engineer.

## 🔥 Focus

- **PostgreSQL (primary)**
  - Replication lag checks
  - Replication slot monitoring
  - Index bloat estimation
  - HA & tuning notes

- **MySQL (secondary)**
  - InnoDB status summaries
  - Basic health/diagnostic queries

- **MongoDB (secondary)**
  - Slow operations inspection examples

## 🧱 Layout

```text
tools/
  postgres/   # Scripts, views, SQL for Postgres
  mysql/      # MySQL helper SQL
  mongodb/    # MongoDB helper scripts

docs/
  postgres-ha-notes.md         # HA patterns, failover notes
  postgres-tuning-checklist.md # Quick tuning checklist

examples/
  postgres/
    docker-compose-primary-replica.yml  # Simple primary + replica demo
