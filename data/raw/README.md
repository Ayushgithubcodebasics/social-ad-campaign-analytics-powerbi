# Raw Data

Full source CSVs for the Meta Ad Campaign dataset.

| File | Rows | Size |
|---|---:|---|
| `ad_events.csv` | 400,000 | ~24 MB |
| `ads.csv` | 200 | ~10 KB |
| `campaigns.csv` | 50 | ~3 KB |
| `users.csv` | 9,841 | ~605 KB |

Data covers **May 7 – August 6, 2025** (event timestamps). Campaign date fields span February–October 2025.

These are the files the Power BI report connects to. If you open the `.pbix` locally, update the data source paths to point here.

**Note:** These are synthetic datasets generated for practice purposes, not real advertising data.

Known data quality issues before you start:
- 225 user IDs stored as scientific notation in `users.csv` → 20,046 unmatched event rows (~5%)
- 225,406 event rows fall outside their campaign's start/end dates (56.4%)
- `total_budget` in `campaigns.csv` is at campaign grain — never SUM after joining to lower grains

Run `python data/audit.py` from the repo root for the full checks.
