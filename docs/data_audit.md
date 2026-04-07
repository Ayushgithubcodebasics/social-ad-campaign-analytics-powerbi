# Data Audit

Before building any visuals I went through all four source files to understand what I was actually working with. There were a few things that would've broken the numbers silently if I hadn't caught them. The Python script that runs all of these checks is at [`data/audit.py`](../data/audit.py).

---

## Source files

| File | Rows | Columns |
|---|---:|---:|
| `ad_events.csv` | 400,000 | 7 |
| `ads.csv` | 200 | 7 |
| `campaigns.csv` | 50 | 6 |
| `users.csv` | 9,841 | 7 |

Event data spans **May 7 – August 6, 2025** (roughly 3 months). Campaign date fields span a wider window (Feb 13 – Oct 12, 2025), which matters for section 3 below.

---

## What was clean

Primary key uniqueness held across all four tables — no duplicate `event_id`, `ad_id`, `campaign_id`, or `user_id` values. That's the baseline check I always run first.

The main join chain was solid:

- `ad_events → ads` on `ad_id`: **100.00%** ✅
- `ads → campaigns` on `campaign_id`: **100.00%** ✅

Every event traces back to a known ad, and every ad traces back to a known campaign. The core analytics chain is reliable.

---

## What needed attention

### 1. User join gap — 5.01% of events have no user match

`ad_events → users` join on `user_id` covers **94.99%** of events, leaving **20,046 rows** unmatched.

The root cause is **two separate Excel CSV-opening artifacts** that together corrupted **406 user IDs** in `users.csv`:

**Artifact A — Scientific notation conversion (289 IDs):**
User IDs in `ad_events.csv` are 5-character hex strings (e.g., `50e00`, `12e01`). When `users.csv` is opened in Excel, IDs containing `e` are silently interpreted as scientific notation numbers:
- `50e00` → 50 × 10⁰ = 50 → stored as `5.00E+01`
- `07e01` → 7 × 10¹ = 70 → stored as `7.00E+01`
- `12e01` → 12 × 10¹ = 120 → stored as `1.20E+02`

The `ad_events.csv` file retained the original `50e00` string. The join breaks because `50e00 ≠ 5.00E+01`.

**Artifact B — Leading-zero stripping (117 IDs):**
User IDs that are all-numeric (e.g., `00062`, `00067`) lose their leading zeros when Excel opens the CSV, treating them as integers:
- `00062` → Excel strips zeros → stored as `62`
- `00095` → Excel strips zeros → stored as `95`

The `ad_events.csv` file retained `00062`. The join breaks because `00062 ≠ 62`. This artifact is not mentioned in typical scientific-notation data quality discussions but causes exactly the same downstream join failure.

**Total: 289 sci-notation + 117 leading-zero-stripped = 406 corrupted user IDs.**

Impact in the report: those 20,046 events still count toward impressions, clicks, purchases, and all event-type KPIs. They don't appear in any breakdown by gender, age, country, or interest. Any user-level analysis has a ~5% coverage gap baked in. The issue is a source problem, not a transformation problem — it wasn't "fixed" in Power Query, but it is documented and accounted for in all demographic chart interpretation.

### 2. Campaign window violations — 56.4% of events fall outside campaign dates

When I joined events through to campaigns and compared `timestamp` against `start_date` and `end_date`, **225,406 event rows fell outside their campaign's active window** — more than half the event table.

Event data runs from May 7 to August 6, 2025. Campaign dates span February through October 2025, with different windows per campaign. The misalignment is too large to be a timezone or formatting artifact — either the dataset was assembled by pulling events from a broader collection period than the campaigns were defined over, or campaign dates were updated after events were logged. Either way, campaign dates are not reliable event boundaries and no analysis in the report uses them to filter events.

### 3. Budget fanout — the one that looks fine until it isn't

`total_budget` is stored once per campaign — one value, one row. The moment you join it to a lower grain and aggregate:

| Aggregation grain | Total | Inflation |
|---|---:|---:|
| Campaign (correct) | $2,535,923.78 | ×1 |
| After joining to ads | $10,222,673.08 | ×4 |
| After joining to events | $20,467,767,701.97 | ×8,071 |

The $20 billion figure is mathematically correct given a naive join + SUM — it passes silently and produces a card showing a very large number with no obvious error. Without checking the grain, you'd never catch it.

The fix: all budget measures in the report aggregate from the campaigns table directly. The blended CPA ($1,248.61 = $2,535,923.78 ÷ 2,031 purchases) uses this correct campaign-grain total. Budget does not change when switching between Facebook and Instagram pages — this is correct behavior, because the source data does not split `total_budget` by platform.

---

## Sample vs. full source

The files in `data/sample/` are a small clean subset: 10 campaigns, 63 ads, 1,810 users, 2,000 events. Filtered to only include rows that pass all four checks above — complete joins, no scientific notation, events mostly within campaign windows. They're there to show the schema without running the full 400k-row file.

To run the audit against the full source:
```bash
python data/audit.py
```

To run against the sample only:
```bash
python data/audit.py --sample
```
