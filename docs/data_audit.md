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

The root cause: 225 user IDs in the users file are stored in scientific notation — values like `1.20E+01`, `5.00E+01`, `7.00E+01`. This is a known spreadsheet export problem. When Excel opens a CSV with large numeric-looking IDs, it silently converts them to scientific notation. The `user_id` values in `ad_events.csv` stayed as strings, so the join breaks for those 225 users.

Impact in the report: those 20,046 events still count toward impressions, clicks, purchases, and all event-type KPIs. They just don't appear in any breakdown by gender, age, country, or interest. Any user-level analysis has a ~5% coverage gap baked in. I didn't try to fix this in Power Query — it's a source issue, not a transformation issue — but I'm aware of it when reading demographic charts.

### 2. Campaign window violations — 56.4% of events fall outside campaign dates

When I joined events through to campaigns and compared `timestamp` against `start_date` and `end_date`, **225,406 event rows fell outside their campaign's active window** — more than half the event table.

Event data runs from May 7 to August 6, 2025. But campaign dates span February through October 2025, with different windows per campaign. Most events that appear "outside" are falling into gaps in individual campaign windows rather than outside the overall date range.

I don't have a clean explanation for why the mismatch is this large — either the dataset was assembled by pulling events from a broader collection period than the campaigns were defined over, or campaign dates were updated after events were logged. Either way, I treated campaign dates as unreliable event boundaries and didn't build any analysis that depends on events being contained within their campaign window.

### 3. Budget fanout — the one that looks fine until it isn't

`total_budget` is stored once per campaign — one value, one row. The moment you join it to a lower grain and aggregate:

| Aggregation grain | Total | Inflation |
|---|---:|---:|
| Campaign (correct) | $2,535,923.78 | ×1 |
| After joining to ads | $10,222,673.08 | ×4 |
| After joining to events | $20,467,767,701.97 | ×8,071 |

The $20 billion figure is mathematically correct given a naive join + SUM — it passes silently and produces a card showing a very large number with no obvious error. Without checking the grain, you'd never catch it.

The fix: all budget measures in the report are written to aggregate from the campaigns table directly. The budget KPIs show campaign-level allocated budget. I'm explicit in the walkthrough that the budget doesn't change by platform or ad type — because the source data doesn't support that split.

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
