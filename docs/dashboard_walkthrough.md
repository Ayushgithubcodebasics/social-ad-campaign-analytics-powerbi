# Dashboard Walkthrough

**[Open live dashboard](https://app.powerbi.com/view?r=eyJrIjoiMmVhYTNkZTUtYmEzOS00YmYzLWI4MmMtZWI5YjJjZTg0MGI3IiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9)**

---

## Pages

Two main pages — Facebook and Instagram — with a hidden tooltip page. Both pages use the same visual layout. Facebook is the default landing page.

Page-level filters on `ad_platform` separate the two rather than a slicer — this keeps the platform context clean when you open the report without needing to interact with anything first.

---

## Metric switcher

The dropdown at the top left controls which metric every chart responds to. Options: Impressions, Engagements, Clicks, Comments, Purchases, Shares.

Switching it re-renders all charts on the page simultaneously — flipping to "Purchases" immediately shows purchases across gender, age, country, time, and ad type. Chart titles update dynamically using a DAX `SWITCH()` measure: selecting Clicks makes the age chart read "Clicks by Age Group", the country map becomes "Clicks by Country", and so on.

---

## KPI cards (top row)

**Row 1:** Impressions · Clicks · Comments · Shares · Purchases · Engagements

**Row 2:** CTR · Engagement Rate · Conversion Rate · Purchase Rate · Total Budget · Avg Budget/Campaign

Rate metrics are formatted as percentages. Budget shows in USD. The Total Budget card shows $2,535,923.78 on both pages — that's expected, since `total_budget` is stored at campaign grain in the source and isn't split by platform. See [`docs/data_audit.md`](data_audit.md) for why budget at lower grains produces a $20 billion figure.

---

## Visuals

**Engagement by Target Gender (donut chart)**
Shows the selected metric split by `target_gender` from the ads table — Male, Female, or All. This reflects what the ad was targeting, not the actual gender of users who engaged. For actual user gender breakdown, cross-filter with the users table — it's not pre-built as a separate view.

**Target Age Group (bar chart)**
One bar per target age group from the ads table. Shows how ad targeting is distributed across age brackets. Heavy in the 18–34 range, dropping off after 35. Filtered to ages ≤ 65.

**Engagement by Country (bubble map)**
Bubble size scales with the selected metric. US is the dominant bubble by a wide margin — 61,923 Facebook impressions vs the next largest markets. I chose a map over a bar chart here because the geographic spread across US, UK, Canada, India, and Germany is more immediately readable spatially than as ranked bars.

**Analysis by Month (calendar heatmap)**
A matrix-style calendar with conditional formatting based on value intensity. The month slicer is intentionally scoped to this visual only via Edit Interactions — changing the month updates the calendar without collapsing the rest of the report to a single month. Hovering a date cell shows a tooltip page with all key KPIs for that day.

**Weekly Engagement Trend (stacked column chart)**
Stacked by ad type (Image, Video, Stories, Carousel). X-axis is ISO week number from the calendar table. Useful for spotting weeks where one format dominates or overall volume drops.

**Hourly Engagement Trend (area chart)**
X-axis is hour 0–23. In this dataset, hourly patterns are nearly flat — all four time-of-day segments are within 1.5% of each other. The chart confirms this visually rather than hiding it.

**Analysis by Ad Type (matrix)**
Rows are ad types. Columns show abbreviated metric headers: IM (Impressions), CLK (Clicks), CTR, PR (Purchase Rate), ER (Engagement Rate), CR (Conversion Rate). Conditional colour formatting applied per column — high/low values stand out without reading exact numbers.

---

## Filtering and interactions

All visuals cross-filter each other. Clicking a country bubble filters the entire page to that country. Clicking a gender slice, age bar, or ad type row does the same. The only exception is the month slicer, which only affects the calendar heatmap.
