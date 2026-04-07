# Data Audit

Before building any visuals I went through all four source files to understand what I was actually working with. A few things would've broken the numbers silently if I hadn't caught them. The Python script that runs all of these checks is at [`data/audit.py`](../data/audit.py).

---

## Source files

| File | Rows | Columns |
|---|---:|---:|
| `ad_events.csv` | 400,000 | 7 |
| `ads.csv` | 200 | 7 |
| `campaigns.csv` | 50 | 6 |
| `users.csv` | 9,841 | 7 |

Event data spans **May 7 – August 6, 2025**. Campaign date fields span a wider window (Feb 13 – Oct 12, 2025), which matters for issue 2 below.

---

## Join coverage

Primary key uniqueness held across all four tables — no duplicate `event_id`, `ad_id`, `campaign_id`, or `user_id` values.

The main join chain:

- `ad_events → ads` on `ad_id`: **100.00%** ✅
- `ads → campaigns` on `campaign_id`: **100.00%** ✅
- `ad_events → users` on `user_id`: **94.99%** ⚠️

Every event traces back to a known ad and campaign. The user join is the problem.

---

## 1. User join gap — 5.01% of events have no user match

`ad_events → users` on `user_id` leaves **20,046 rows** unmatched. The root cause is **two separate Excel CSV-opening artifacts** that corrupted **406 user IDs** in `users.csv`:

**Artifact A — Scientific notation conversion (289 IDs):**
User IDs in `ad_events.csv` are 5-character hex strings (e.g., `50e00`, `12e01`). When `users.csv` is opened in Excel, IDs containing `e` get silently interpreted as scientific notation:
- `50e00` → 50 × 10⁰ = 50 → stored as `5.00E+01`
- `07e01` → 7 × 10¹ = 70 → stored as `7.00E+01`

`ad_events.csv` retained the original `50e00`. Join breaks because `50e00 ≠ 5.00E+01`.

**Artifact B — Leading-zero stripping (117 IDs):**
All-numeric user IDs (e.g., `00062`, `00067`) lose their leading zeros when Excel opens the CSV:
- `00062` → stored as `62`

`ad_events.csv` retained `00062`. Join breaks because `00062 ≠ 62`.

**Total: 289 sci-notation + 117 leading-zero-stripped = 406 corrupted user IDs.**

Those 20,046 unmatched events still count toward impressions, clicks, and purchases. They don't appear in any demographic breakdown (gender, age, country, interest). Any user-level analysis has a ~5% coverage gap. This wasn't fixed in Power Query — it's a source problem that's documented and accounted for in interpretation.

---

## 2. Campaign window violations — 56.4% of events fall outside campaign dates

225,406 events fall outside their linked campaign's start/end dates. The events span May 7 – August 6, 2025; campaign dates span February–October 2025. A 56.4% mismatch is too large to be a timezone artifact — campaign dates simply aren't reliable event boundaries in this dataset. They're not used as analysis filters.

---

## 3. Budget fanout

`total_budget` is stored at campaign grain — one value per campaign, not split by platform or ad type. Joining it down and summing:

| Aggregation grain | Total | Multiplier |
|---|---:|---:|
| Campaign (correct) | $2,535,923.78 | 1× |
| Joined to ads | $10,222,673.08 | 4× |
| Joined to events | $20,467,767,701.97 | 8,071× |

Power BI doesn't throw an error — it just shows a $20 billion budget card. All budget measures in the report aggregate directly from the campaigns table to avoid this.
