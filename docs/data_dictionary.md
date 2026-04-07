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
| `total_budget` | decimal | total allocated budget in USD — campaign grain only |

`total_budget` is the one to watch. It's a campaign-level figure and only makes sense when aggregated from the campaigns table directly. Joining it down to ads or events and summing inflates the number by 4× or 8,071× respectively. See [`docs/data_audit.md`](data_audit.md) for the full breakdown.

---

## ads

| Column | Type | Notes |
|---|---|---|
| `ad_id` | integer | primary key |
| `campaign_id` | integer | foreign key to campaigns |
| `ad_platform` | string | `Facebook` or `Instagram` |
| `ad_type` | string | `Image`, `Video`, `Stories`, or `Carousel` |
| `target_gender` | string | `Male`, `Female`, or `All` — what the ad was targeting, not actual user gender |
| `target_age_group` | string | e.g. `18-24`, `25-34`, `35-44` |
| `target_interests` | string | comma-separated interest categories |

`ad_platform` is how the report separates Facebook and Instagram — page-level filters on this field. `target_gender` comes from this table, so gender breakdowns reflect ad targeting strategy, not the actual gender of users who engaged (those come from the users table).

---

## users

| Column | Type | Notes |
|---|---|---|
| `user_id` | string | primary key — note: 225 IDs stored as scientific notation in source (`1.20E+01`), causing a 5% join gap with ad_events |
| `user_gender` | string | `Male`, `Female`, or `Other` — actual user gender |
| `user_age` | integer | exact age in years |
| `age_group` | string | banded bucket: `16-17`, `18-24`, `25-34`, `35-44`, `45-54`, `55-65` |
| `country` | string | user's country |
| `location` | string | city/location within country |
| `interests` | string | comma-separated interest categories |

The distinction between `target_gender` (ads table) and `user_gender` (users table) is meaningful. In this dataset, female-targeted ads dominate targeting allocation (43.4% of engagements), but actual male users are the majority of engagers (54.4%). These two fields measure different things.

---

## ad_events

| Column | Type | Notes |
|---|---|---|
| `event_id` | integer | primary key |
| `ad_id` | integer | foreign key to ads |
| `user_id` | string | foreign key to users — 5.01% have no match due to the scientific notation issue |
| `timestamp` | datetime | when the event occurred (format: `YYYY-MM-DD HH:MM:SS`) |
| `day_of_week` | string | derived field, e.g. `Monday` — present in source, not recalculated |
| `time_of_day` | string | `Morning`, `Afternoon`, `Evening`, or `Night` — derived field |
| `event_type` | string | type of interaction — see below |

**Event types:**
| Value | Count (full source) | Notes |
|---|---|---|
| `Impression` | 339,812 | ad was displayed |
| `Click` | 40,079 | user clicked the ad |
| `Like` | 12,013 | user liked the ad |
| `Comment` | 4,108 | user commented |
| `Share` | 1,957 | user shared the ad |
| `Purchase` | 2,031 | user made a purchase |

`Like` is tracked separately in the dashboard but excluded from the Engagements measure (defined as Clicks + Comments + Shares only).

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
