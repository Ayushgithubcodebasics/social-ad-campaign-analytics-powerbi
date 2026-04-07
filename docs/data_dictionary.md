# Data Dictionary

Field-level reference for all four tables in the model.

---

## Table overview

| Table | Grain | Primary key | Role in model |
|---|---|---|---|
| `campaigns` | one row per campaign | `campaign_id` | campaign names, dates, and budget |
| `ads` | one row per ad creative | `ad_id` | platform, format, and targeting metadata |
| `users` | one row per user | `user_id` | audience demographics and interests |
| `ad_events` | one row per interaction event | `event_id` | fact table — all KPIs are derived from here |

---

## campaigns

| Column | Type | Notes |
|---|---|---|
| `campaign_id` | integer | primary key |
| `name` | string | e.g. `Campaign_4_Summer`, `Campaign_9_Launch` |
| `start_date` | date | campaign start (format: DD-MM-YYYY in source) |
| `end_date` | date | campaign end |
| `duration_days` | integer | days between start and end |
| `total_budget` | decimal | total allocated budget in USD — campaign grain only. This is the one to be careful with: joining it down to ads or events and summing inflates it by 4× or 8,071× respectively. See [`docs/data_audit.md`](data_audit.md). |

---

## ads

| Column | Type | Notes |
|---|---|---|
| `ad_id` | integer | primary key |
| `campaign_id` | integer | foreign key to campaigns |
| `ad_platform` | string | `Facebook` or `Instagram` — page-level filters in the report use this field |
| `ad_type` | string | `Image`, `Video`, `Stories`, or `Carousel` |
| `target_gender` | string | `Male`, `Female`, or `All` — what the ad was targeting, not actual user gender |
| `target_age_group` | string | e.g. `18-24`, `25-34`, `35-44` |
| `target_interests` | string | comma-separated interest categories |

`target_gender` comes from this table. The actual gender of users who engaged comes from the users table. They don't match — female-targeted ads account for 43.4% of targeting allocation, but 55.2% of actual engagers are male.

---

## users

| Column | Type | Notes |
|---|---|---|
| `user_id` | string | primary key — 406 IDs are corrupted in source: 289 converted to scientific notation by Excel (`50e00` → `5.00E+01`) and 117 with leading zeros stripped (`00062` → `62`). These cause a 5.01% join gap with ad_events. |
| `user_gender` | string | `Male`, `Female`, or `Other` |
| `user_age` | integer | exact age in years |
| `age_group` | string | banded bucket: `16-17`, `18-24`, `25-34`, `35-44`, `45-54`, `55-65` |
| `country` | string | user's country |
| `location` | string | city/location within country |
| `interests` | string | comma-separated interest categories |

---

## ad_events

| Column | Type | Notes |
|---|---|---|
| `event_id` | integer | primary key |
| `ad_id` | integer | foreign key to ads |
| `user_id` | string | foreign key to users — 5.01% have no match due to both Excel artifacts described above (scientific notation + leading-zero stripping) |
| `timestamp` | datetime | when the event occurred (`YYYY-MM-DD HH:MM:SS`) |
| `day_of_week` | string | pre-computed in source, not recalculated in Power Query |
| `time_of_day` | string | `Morning`, `Afternoon`, `Evening`, or `Night` — pre-computed in source |
| `event_type` | string | type of interaction — see below |

**Event types:**
| Value | Count (full source) | Notes |
|---|---|---|
| `Impression` | 339,812 | ad was displayed |
| `Click` | 40,079 | user clicked the ad |
| `Like` | 12,013 | user liked the ad — tracked separately, excluded from Engagements |
| `Comment` | 4,108 | user commented |
| `Share` | 1,957 | user shared the ad |
| `Purchase` | 2,031 | user made a purchase |

---

## Calendar table (DAX-generated)

Built in Power BI using `CALENDARAUTO()` seeded from the min/max of a derived `event_date` column in `ad_events`. Not in the source files — created entirely in the model.

| Column | Description |
|---|---|
| `Date` | unique date — primary key, marked as date table |
| `Month Name` | three-letter month abbreviation |
| `Day Name` | three-letter day abbreviation |
| `Day Number` | day of month (numeric) |
| `Weekday` | numeric weekday, Monday=1 |
| `Week Number` | ISO week number |
