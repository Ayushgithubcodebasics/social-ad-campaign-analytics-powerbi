# Sample Data

A small clean subset of the full dataset for schema review.

| File | Rows |
|---|---|
| `campaigns_sample.csv` | 10 campaigns |
| `ads_sample.csv` | 63 ads |
| `users_sample.csv` | 1,810 users |
| `ad_events_sample.csv` | 2,000 events |

These won't reproduce the dashboard numbers — the live report runs off the full 400k-row source in `data/raw/`.

The sample was filtered to clean rows only: complete joins, no scientific notation in user IDs, all event timestamps within campaign windows. The data quality issues in [`docs/data_audit.md`](../docs/data_audit.md) only appear in the full source.

To run the audit against the sample:
```bash
python data/audit.py --sample
```
