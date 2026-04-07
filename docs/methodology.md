# Methodology

How the data model was built, why certain decisions were made, and where the tricky parts were.

---

## Data model structure

Four tables in a snowflake arrangement:

- `campaigns` → `ads` (1:many, on `campaign_id`)
- `ads` → `ad_events` (1:many, on `ad_id`)
- `users` → `ad_events` (1:many, on `user_id`)
- `calendar table` → `ad_events` (1:many, on `event_date`)

`ad_events` is the fact table — 400,000 rows, one per interaction event. All four dimension tables feed into it, so filters applied to campaigns, ads, or users propagate correctly through to the event counts.

I also added a fifth connection: a DAX-generated calendar table. This isn't in the source data — I built it in Power BI using `CALENDARAUTO()` seeded from the min/max of a derived `event_date` column. The reason: DAX time intelligence functions (`DATEADD`, `SAMEPERIODLASTYEAR`, etc.) require a proper date table with contiguous dates and a marked date field. Without it, those functions return incorrect results or just blank. The `event_date` column itself was extracted from the raw `timestamp` field (which comes in as a full datetime) using `DATEVALUE([timestamp])`, then the column data type was changed to Date.

---

## KPI definitions

All event-based KPIs follow the same pattern — `COUNTROWS(FILTER(ad_events, ad_events[event_type] = "..."))`. The string literal has to match exactly what's in the source data: it's case sensitive. "Click" works. "click" breaks.

**Engagements = Clicks + Comments + Shares**

Likes are in the source data (12,013 on Facebook, 4,508 on Instagram) but I left them out of the Engagements measure. A like is a very low-effort interaction — one tap, no commitment. Clicks, comments, and shares all represent more deliberate engagement. Including likes would inflate the engagement number without adding analytical value and makes the metric harder to explain consistently.

**CTR, Engagement Rate, Conversion Rate, Purchase Rate** all use `DIVIDE()` with 0 as the alternate result:

```dax
CTR = DIVIDE([Clicks], [Impressions], 0)
```

The `0` handles the zero-denominator case cleanly. Without it, blank denominators produce blank cells rather than 0%, which shows up as visual gaps in charts and tooltips.

**Conversion Rate vs Purchase Rate** — these have different denominators and mean different things:
- Conversion Rate = Purchases ÷ Clicks (of people who clicked, what % bought)
- Purchase Rate = Purchases ÷ Impressions (of all ad views, what % ended in a purchase)

Purchase Rate is always lower. Conversion Rate tells you about the post-click experience — landing page quality, offer strength. Purchase Rate tells you about overall campaign efficiency from first exposure. Both are useful and I kept both on the report.

---

## Budget handling

`total_budget` is stored at campaign grain — one value per campaign, not split by platform or ad. Joining it down to the ads or events grain and then using SUM multiplies it by the number of rows at that grain. The result looks plausible but is completely wrong.

Real total: $2,535,923.78. At event grain: $20,467,767,701.97. This is one of the trickier data modelling gotchas because Power BI doesn't throw an error — it just shows a $20 billion card and moves on.

All budget measures in the report are written to aggregate at campaign grain only. The budget cards don't change when you switch between Facebook and Instagram — that's expected and correct, since the source data doesn't split budget by platform.

---

## Dynamic field parameter

Rather than separate pages for each metric, I created a Power BI field parameter in the Modeling tab. The parameter holds: Impressions, Engagements, Clicks, Comments, Purchases, Shares.

Every chart uses the parameter value as its Y-axis measure. Switching the dropdown at the top re-renders all charts simultaneously for the selected metric. For chart titles, I built a DAX measure using `SWITCH()` over the parameter index to generate dynamic strings like "Engagements by Country" or "Clicks by Age" — these update automatically when the parameter changes.

---

## Cross-filter behavior

Power BI's default interaction mode is "highlight" — clicking a slice in the gender donut dims everything else but doesn't actually change the numbers in other visuals. I changed all visuals to "filter" mode using Edit Interactions. So clicking a country bubble on the map now filters every other visual on the page to that country. Clicking an age bar filters the whole report to that age group.

The exception: the month slicer on the calendar heatmap. I blocked that from filtering the rest of the report, because the calendar is meant to stay in its own date context while the other charts reflect the broader filter state.

---

## Two-page structure

Facebook and Instagram are separate pages rather than a slicer. Each page has a page-level filter on `ad_platform`. This keeps the platforms fully separated — no risk of cross-platform totals appearing — and lets you open the report on either platform cleanly without needing to interact with a filter first.

Navigation buttons at the top of each page link to the other page. This is a Design Mode button linked to the page navigation bookmark action rather than a slicer, which keeps the URL clean.
