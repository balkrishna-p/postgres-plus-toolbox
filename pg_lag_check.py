#!/usr/bin/env python3
"""
pg_lag_check.py

Simple PostgreSQL replication lag checker for a physical standby.

It connects using environment variables:
  PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE

Example:
  export PGHOST=localhost
  export PGPORT=5432
  export PGUSER=postgres
  export PGPASSWORD=secret
  export PGDATABASE=postgres
  python pg_lag_check.py
"""

import os
import sys
from typing import Optional

import psycopg2
import psycopg2.extras


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        print(f"ERROR: environment variable {name} is not set and no default provided.", file=sys.stderr)
        sys.exit(1)
    return value


def connect():
    conn = psycopg2.connect(
        host=get_env("PGHOST", "localhost"),
        port=get_env("PGPORT", "5432"),
        user=get_env("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", ""),
        dbname=get_env("PGDATABASE", "postgres"),
    )
    return conn


def fetch_lag(cur) -> Optional[float]:
    """
    Returns lag in seconds (float) or None if pg_last_xact_replay_timestamp is NULL
    (which usually means this is not a physical standby).
    """
    cur.execute(
        """
        SELECT
            now() AS current_time,
            pg_last_xact_replay_timestamp() AS replay_time,
            EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) AS replay_delay_seconds
        """
    )
    row = cur.fetchone()
    current_time, replay_time, replay_delay_seconds = row

    print(f"Current time:            {current_time}")
    print(f"Replay time:             {replay_time}")

    if replay_time is None:
        # Not a physical standby, or nothing replayed yet
        return None

    print(f"Replay delay (seconds):  {replay_delay_seconds:.3f}")
    return float(replay_delay_seconds)


def main():
    try:
        conn = connect()
    except Exception as e:
        print(f"ERROR: could not connect to PostgreSQL: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            lag_seconds = fetch_lag(cur)

        if lag_seconds is None:
            print(
                "WARN: pg_last_xact_replay_timestamp() is NULL.\n"
                "This usually means this server is not a physical standby, "
                "or no WAL has been replayed yet."
            )
            sys.exit(2)

        # Simple exit codes that can be used in monitoring:
        #  0 = OK
        #  1 = lag above warning/critical thresholds (not implemented here)
        # For now always exit 0 if we got a numeric lag.
        sys.exit(0)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
