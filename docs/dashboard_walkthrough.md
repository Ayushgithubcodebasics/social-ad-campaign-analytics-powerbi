# Dashboard Walkthrough

**[Open live dashboard](https://app.powerbi.com/view?r=eyJrIjoiMmVhYTNkZTUtYmEzOS00YmYzLWI4MmMtZWI5YjJjZTg0MGI3IiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9)**

---

## Pages

Two main pages — Facebook and Instagram — with a hidden tooltip page. Both pages use the same visual layout, so comparing them side by side is straightforward. Facebook is the default landing page.

Page-level filters on `ad_platform` separate the two — each page is filtered at the page level rather than using a slicer, so the platform context is always clean when you open the report.

---

## Metric switcher

The dropdown at the top left controls which metric every chart responds to. Options: Impressions, Engagements, Clicks, Comments, Purchases, Shares.

Switching it re-renders all charts on the page simultaneously — so flipping to "Purchases" immediately shows purchases across gender, age, country, time, and ad type without touching each chart individually. Chart titles update dynamically too using a DAX `SWITCH()` measure: selecting Clicks makes the age chart read "Clicks by Age Group", the country map becomes "Clicks by Country", and so on.

---

## KPI cards (top row)

**Row 1:** Impressions · Clicks · Comments · Shares · Purchases · Engagements

**Row 2:** CTR · Engagement Rate · Conversion Rate · Purchase Rate · Total Budget · Avg Budget/Campaign

Rate metrics are formatted as percentages. Budget shows in USD.

Facebook reference numbers from the full dataset: 215,972 impressions, 25,389 clicks, 11.76% CTR, 5.21% conversion rate, $2.54M total budget. The Total Budget card doesn't change when you switch platforms — that's expected, because `total_budget` is stored at campaign grain in the source and isn't split by platform.

---

## Visuals

**Engagement by Target Gender (donut chart)**
Shows the selected metric split by `target_gender` from the ads table — Male, Female, or All. This reflects what the ad was targeting, not the actual gender of users who engaged. Female-targeted ads account for 43.4% of Facebook engagements on this metric. For actual user gender breakdown, you'd need to cross-filter with the users table — not directly available as a pre-built view in this report.

**Target Age Group (bar chart)**
One bar per target age group from the ads table. Shows how the ad spend is distributed across age targeting brackets. Heavy targeting in the 18–34 range, dropping off after 35. Filtered to ages ≤ 65.

**Engagement by Country (bubble map)**
Bubble size scales with the selected metric. Hovering shows country name and value. US is the largest bubble by a wide margin — 61,923 Facebook impressions vs the next largest markets.

**Analysis by Month (calendar heatmap)**
A matrix-style calendar with conditional formatting based on value intensity. The month slicer above it controls which month is shown. The slicer is intentionally scoped to this visual only via Edit Interactions — changing the month only updates the calendar, not the other charts. This lets you browse dates without collapsing the rest of the report to a single month.

Hovering a date cell shows a tooltip page with all key KPIs for that day.

**Weekly Engagement Trend (stacked column chart)**
Stacked by ad type (Image, Video, Stories, Carousel). X-axis is ISO week number from the calendar table. Shows volume and format composition by week. Useful for spotting any weeks where one format dominates or where overall volume drops.

**Hourly Engagement Trend (area chart)**
X-axis is hour 0–23 from the `timestamp` field. In this dataset, hourly patterns are almost flat — all four time-of-day segments (Morning, Afternoon, Evening, Night) are within 1.5% of each other. The chart confirms this visually rather than hiding it.

**Analysis by Ad Type (matrix)**
Rows are ad types. Columns show abbreviated metric headers: IM (Impressions), CLK (Clicks), CTR, PR (Purchase Rate), ER (Engagement Rate), CR (Conversion Rate). Conditional colour formatting applied per column — high/low values stand out immediately without needing to read exact numbers.

On Facebook: Stories leads on impressions and conversion rate. Video leads on engagement rate and CTR. Image trails on both.

---

## Filtering and interactions

All visuals cross-filter each other. Clicking a country bubble filters the entire page to that country — the gender donut, age bar, time chart, and ad type matrix all update to show that country's data. Same for clicking a gender slice, age bar, or ad type row.

The only exception is the month slicer, which only affects the calendar heatmap. Everything else responds to cross-filter clicks from any other visual.

---

## Notes

The Total Budget card on both pages shows $2,535,923.78 regardless of which platform page you're on. This is correct — budget data in the source isn't split by platform, and faking a split would produce misleading numbers. See [`docs/data_audit.md`](data_audit.md) for why budget aggregation at lower grains produces a $20 billion figure.
