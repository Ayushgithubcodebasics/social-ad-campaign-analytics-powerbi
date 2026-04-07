# Methodology

How the data model was built, why certain decisions were made, and where the tricky parts were.

---

## Data model structure

Four tables in a snowflake arrangement:

- `campaigns` → `ads` (1:many, on `campaign_id`)
- `ads` → `ad_events` (1:many, on `ad_id`)
- `users` → `ad_events` (1:many, on `user_id`)
- `calendar table` → `ad_events` (1:many, on `event_date`)

`ad_events` is the fact table — 400,000 rows, one per interaction event. All four dimension tables feed into it, so filters on campaigns, ads, or users propagate correctly through to the event counts.

I also built a DAX calendar table using `CALENDARAUTO()` seeded from the min/max of a derived `event_date` column. DAX time intelligence functions (`DATEADD`, `SAMEPERIODLASTYEAR`, etc.) need a proper contiguous date table with a marked date field — without it they return blank or wrong results. One thing that took me longer than I'd like to admit: `CALENDARAUTO()` requires the source column to already be typed as `Date`, not `DateTime`. The `event_date` column is extracted from the raw `timestamp` field using `DATEVALUE([timestamp])`, but that returns DateTime by default. Had to explicitly change the column type to Date before `CALENDARAUTO()` would pick it up correctly.

---

## KPI definitions

All event-based KPIs follow the same pattern — `COUNTROWS(FILTER(ad_events, ad_events[event_type] = "..."))`. The string literal has to match exactly what's in the source data: case sensitive. "Click" works. "click" breaks.

**Engagements = Clicks + Comments + Shares**

Likes are in the source data (FB: 7,505 / IG: 4,508) but excluded from Engagements. A like is a low-effort, one-tap interaction. Clicks, comments, and shares represent more deliberate engagement and make the metric easier to explain consistently. Including likes would inflate the number without adding analytical value.

**CTR, Engagement Rate, Conversion Rate, Purchase Rate** all use `DIVIDE()` with 0 as the alternate result:

```dax
CTR = DIVIDE([Clicks], [Impressions], 0)
```

The `0` handles zero-denominator cases cleanly — without it, blank denominators produce blank cells rather than 0%, which shows up as visual gaps in charts.

**Conversion Rate vs Purchase Rate:**
- Conversion Rate = Purchases ÷ Clicks (of people who clicked, what % bought)
- Purchase Rate = Purchases ÷ Impressions (of all ad views, what % ended in a purchase)

Purchase Rate is always lower. Conversion Rate tells you about post-click quality. Purchase Rate tells you about overall campaign efficiency from first exposure. Both are on the report.

---

## Budget handling

`total_budget` is stored at campaign grain — one value per campaign, not split by platform or ad. Joining it down and using SUM multiplies it by the number of rows at that grain. Real total: $2,535,923.78. At event grain: $20,467,767,701.97. Power BI doesn't warn you — it just shows the wrong number.

All budget measures aggregate directly from the campaigns table. The budget cards don't change when you switch between Facebook and Instagram pages — that's correct, not a bug.

---

## Dynamic field parameter

I used a Power BI field parameter (Modeling tab) instead of building separate pages for each metric. The parameter holds: Impressions, Engagements, Clicks, Comments, Purchases, Shares. Every chart uses it as its Y-axis, so switching the dropdown re-renders the whole page at once. For dynamic chart titles, there's a DAX measure using `SWITCH()` over the parameter index — "Clicks by Country", "Engagements by Age", etc., all updating automatically.

---

## Cross-filter behavior

Power BI's default interaction mode is "highlight" — clicking a slice dims everything else but doesn't change the numbers. I changed all visuals to "filter" mode via Edit Interactions, so clicking a country bubble actually filters every other visual on the page to that country.

The exception is the month slicer on the calendar heatmap, which I scoped to that visual only. The calendar is meant to stay in its own date context while the other charts reflect the broader filter state.

---

## Two-page structure

Facebook and Instagram are separate pages rather than a slicer. Each page has a page-level filter on `ad_platform`. Navigation buttons at the top link between pages — these are Design Mode buttons with page navigation bookmark actions, not slicers.
