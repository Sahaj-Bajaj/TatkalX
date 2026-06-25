"""
scripts/init_db.py
──────────────────
Run ONCE to bootstrap the database.

    python scripts/init_db.py

What it does:
  1. Verifies the DB connection
  2. Creates all four tables (idempotent — safe to re-run)
  3. Seeds 100 Indian railway stations (skips if already seeded)
  4. Prints a summary
"""

import sys
import os
import logging
import time

# Allow running from project root: python scripts/init_db.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, get_db, check_connection, Base
from database.models import Station, SearchHistory, Prediction, APIMetric
from database.seed_data import STATIONS_DATA

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

SEPARATOR = "─" * 55


def step(n: int, total: int, label: str):
    logger.info("[%d/%d]  %s", n, total, label)


def main():
    total_steps = 4
    print(f"\n{SEPARATOR}")
    print("  Railway Analytics — Database Initializer")
    print(SEPARATOR)

    # ── Step 1: Verify connection ─────────────────────────────────────────
    step(1, total_steps, "Testing database connection …")
    if not check_connection():
        logger.error(
            "Cannot reach the database.\n"
            "  Check that PostgreSQL is running and DATABASE_URL in .env is correct.\n"
            "  Windows: open Services → PostgreSQL should be 'Running'."
        )
        sys.exit(1)
    logger.info("  ✓  Connected successfully.")

    # ── Step 2: Create tables ─────────────────────────────────────────────
    step(2, total_steps, "Creating tables …")
    Base.metadata.create_all(bind=engine)
    logger.info("  ✓  Tables: stations, search_history, predictions, api_metrics")

    # ── Step 3: Seed stations ─────────────────────────────────────────────
    step(3, total_steps, "Seeding station data …")
    with get_db() as db:
        existing = db.query(Station).count()
        if existing >= len(STATIONS_DATA):
            logger.info(
                "  ⟳  Already seeded (%d stations). Skipping.", existing
            )
        else:
            # Upsert-style: only insert codes that don't exist yet
            existing_codes = {
                row[0]
                for row in db.query(Station.station_code).all()
            }
            to_insert = [
                s for s in STATIONS_DATA if s["code"] not in existing_codes
            ]

            for s in to_insert:
                db.add(
                    Station(
                        station_code=s["code"],
                        station_name=s["name"],
                        city=s["city"],
                        state=s["state"],
                        zone=s["zone"],
                        latitude=s["latitude"],
                        longitude=s["longitude"],
                        is_major=s["is_major"],
                    )
                )
            # commit handled by context manager
            logger.info("  ✓  Inserted %d new stations.", len(to_insert))

    # ── Step 4: Verify ────────────────────────────────────────────────────
    step(4, total_steps, "Verifying …")
    with get_db() as db:
        counts = {
            "stations":       db.query(Station).count(),
            "search_history": db.query(SearchHistory).count(),
            "predictions":    db.query(Prediction).count(),
            "api_metrics":    db.query(APIMetric).count(),
        }

    print(f"\n{SEPARATOR}")
    print("  Initialization complete. Table row counts:")
    for table, count in counts.items():
        print(f"    {table:<20}  {count:>6} rows")
    print(SEPARATOR)
    print()
    print("  Next step → add to your .env:")
    print(f"    DATABASE_URL=<your connection string>")
    print()
    print("  Then integrate into your Flask/FastAPI app.")
    print("  See INTEGRATION_GUIDE.md for copy-paste snippets.")
    print(f"{SEPARATOR}\n")


if __name__ == "__main__":
    main()
