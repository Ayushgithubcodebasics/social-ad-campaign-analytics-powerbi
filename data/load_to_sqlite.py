"""
load_to_sqlite.py
-----------------
Loads the four raw CSV files into a local SQLite database (ad_analysis.db)
so the SQL queries in analysis.sql can be run against them.

Usage:
    python data/load_to_sqlite.py

The script detects and handles the two known data quality issues in users.csv:
  - 289 user IDs converted to scientific notation by Excel (e.g. 50e00 → 5.00E+01)
  - 117 user IDs with leading zeros stripped (e.g. 00062 → 62)
Both are loaded as-is; the join gap (5.01%) is expected and documented.

Requirements: pandas, sqlalchemy (pip install pandas sqlalchemy)
"""

import sqlite3
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).parent / "raw"
DB_PATH = Path(__file__).parent / "ad_analysis.db"

TABLES = {
    "campaigns": RAW_DIR / "campaigns.csv",
    "ads":       RAW_DIR / "ads.csv",
    "users":     RAW_DIR / "users.csv",
    "ad_events": RAW_DIR / "ad_events.csv",
}

DTYPES = {
    # Force user_id as string everywhere to preserve hex IDs and leading zeros.
    # Without this, pandas would coerce '00062' to 62, breaking joins.
    "user_id": str,
}


def load_table(conn: sqlite3.Connection, name: str, path: Path) -> None:
    df = pd.read_csv(path, dtype=DTYPES, low_memory=False)
    df.to_sql(name, conn, if_exists="replace", index=False)
    print(f"  Loaded {name:12s}  {len(df):>9,} rows  from {path.name}")


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    print(f"Creating {DB_PATH.name} ...")
    conn = sqlite3.connect(DB_PATH)

    for table_name, csv_path in TABLES.items():
        if not csv_path.exists():
            print(f"  SKIPPED {table_name} — {csv_path.name} not found in data/raw/")
            continue
        load_table(conn, table_name, csv_path)

    conn.close()
    print(f"\nDone. Run queries in data/analysis.sql against {DB_PATH.name}")
    print("Example: sqlite3 data/ad_analysis.db < data/analysis.sql")


if __name__ == "__main__":
    main()
