# Meta Ad Campaign Analytics — Power BI

A Power BI report analyzing Facebook and Instagram ad performance built on a synthetic dataset — 50 campaigns, 200 ads, 9,841 users, 400,000 events spanning May–August 2025.

**[→ Live dashboard](https://app.powerbi.com/view?r=eyJrIjoiMmVhYTNkZTUtYmEzOS00YmYzLWI4MmMtZWI5YjJjZTg0MGI3IiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9)**

The working `.pbix` file is [`meta_ad_performance.pbix`](meta_ad_performance.pbix) in the root of this repo. Raw source data is in [`data/raw/`](data/raw/).

---

## Numbers at a glance

### Facebook
| Metric | Value |
|---|---|
| Impressions | 215,972 |
| Clicks | 25,389 |
| Engagements (Clicks + Comments + Shares) | 29,296 |
| Purchases | 1,323 |
| CTR | 11.76% |
| Engagement Rate | 13.56% |
| Conversion Rate | 5.21% |
| Purchase Rate | 0.61% |
| Total Budget | $2,535,923.78 |
| Avg Budget per Campaign | $50,718.48 |

### Instagram
| Metric | Value |
|---|---|
| Impressions | 123,840 |
| Clicks | 14,690 |
| Purchases | 708 |
| CTR | 11.86% |
| Engagement Rate | 13.60% |
| Conversion Rate | 4.82% |

Facebook has more volume. Instagram has a slightly better CTR but lower conversion rate — more clicks, fewer purchases per click.

---

## What the data actually shows

**The funnel drops hard after the click.** Facebook: 215,972 impressions → 25,389 clicks → 1,323 purchases. That's a 94.8% drop-off between click and purchase. CTR is strong at 11.76% (industry average is 1–2%), so the ads are working. The issue is post-click.

**Stories leads on reach, Video leads on efficiency.** On Facebook, Stories gets the most impressions (71,537) and the best conversion rate (5.52%). Video has the smallest reach (45,770) but the highest engagement rate (13.74%) and second-best CTR (11.88%). Image underperforms on both reach and conversion.

| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Purchase Rate | Eng. Rate |
|---|---:|---:|---:|---:|---:|---:|
| Carousel | 47,752 | 5,602 | 11.73% | 5.05% | 0.59% | 13.44% |
| Image | 50,913 | 5,943 | 11.67% | 4.91% | 0.57% | 13.46% |
| Stories | 71,537 | 8,406 | 11.75% | 5.52% | 0.65% | 13.61% |
| Video | 45,770 | 5,438 | 11.88% | 5.22% | 0.62% | 13.74% |

**The US dominates, not India or Brazil.** When you actually look at the engagement numbers, the United States leads with 13,279 engagements, followed by UK (6,572), Canada (4,345), India (4,170), Germany (3,695). India has the highest CTR (12.03%) and Canada has the highest conversion rate (5.44%) — but they're not the volume leaders. 

**Target gender vs. actual user gender don't match.** Female-targeted ads account for 43.4% of engagements (by ad targeting). But the actual users engaging on Facebook are predominantly male — 54.4% male vs 34.2% female. The ads are targeting females, but males are responding more. That's worth investigating.

**Time-of-day patterns are nearly flat.** Afternoon: 11,610 engagements. Evening: 11,574. Morning: 11,520. Night: 11,440. Under 2% spread between the peak and the slowest window. The "schedule ads in the afternoon" advice gets thrown around a lot — this dataset doesn't really support it.

---

## Data quality issues found

Three things I caught before building any visuals:

1. **User join gap (5.01%)** — 20,046 event rows have no matching user. Root cause: 225 user IDs in the users file stored in scientific notation (`1.20E+01`, `5.00E+01`, etc.) due to a spreadsheet export issue. These events still count in impression/click/purchase totals but drop out of demographic breakdowns.

2. **Campaign window violations (56.4%)** — 225,406 events fall outside their campaign's start/end dates. Events span May 7 – August 6, 2025. Campaign dates span February–October 2025. The windows don't match the event distribution. Avoided any analysis that treats campaign dates as reliable event boundaries.

3. **Budget fanout** — `total_budget` is one row per campaign. Join it down and SUM, and the number explodes:

| Aggregation grain | Total | Multiplier |
|---|---:|---:|
| Campaign (correct) | $2,535,923.78 | 1× |
| Joined to ads | $10,222,673.08 | 4× |
| Joined to events | $20,467,767,701.97 | 8,071× |

All budget measures in the report pull directly from the campaigns table to avoid this.

The Python script that runs all these checks is at [`data/audit.py`](data/audit.py).

---

## Data model

Four tables in a snowflake schema:

```
campaigns ──< ads ──< ad_events >── users
                           │
                      calendar table (DAX)
```

- `campaigns → ads` on `campaign_id` (1:many)
- `ads → ad_events` on `ad_id` (1:many)
- `users → ad_events` on `user_id` (1:many)
- `calendar table → ad_events` on `event_date` (1:many)

`ad_events` is the fact table. The calendar table was built in DAX using `CALENDARAUTO()` off a derived `event_date` column extracted from the raw timestamp field — necessary for DAX time intelligence to work reliably.

---

## DAX measures

```dax
Impressions      = COUNTROWS(FILTER(ad_events, ad_events[event_type] = "Impression"))
Clicks           = COUNTROWS(FILTER(ad_events, ad_events[event_type] = "Click"))
Comments         = COUNTROWS(FILTER(ad_events, ad_events[event_type] = "Comment"))
Shares           = COUNTROWS(FILTER(ad_events, ad_events[event_type] = "Share"))
Purchases        = COUNTROWS(FILTER(ad_events, ad_events[event_type] = "Purchase"))
Engagements      = [Clicks] + [Comments] + [Shares]
CTR              = DIVIDE([Clicks], [Impressions], 0)
Engagement Rate  = DIVIDE([Engagements], [Impressions], 0)
Conversion Rate  = DIVIDE([Purchases], [Clicks], 0)
Purchase Rate    = DIVIDE([Purchases], [Impressions], 0)
Total Budget     = SUM(campaigns[total_budget])
Avg Budget       = AVERAGE(campaigns[total_budget])
```

Likes exist in the source data but are excluded from Engagements — defined as Clicks + Comments + Shares to capture only high-intent interactions.

---

## Dashboard previews

### Facebook overview
![Facebook overview](images/dashboard_overview.png)

### Instagram page
![Instagram](images/dashboard_instagram.png)

### Data model
![Data model](images/data_model.png)

---

## Repo structure

```
social-ad-campaign-analytics-powerbi/
├── README.md
├── .gitignore
├── meta_ad_performance.pbix          ← Power BI working file
├── docs/
│   ├── findings.md                   ← analysis and recommendations
│   ├── data_audit.md                 ← data quality checks
│   ├── data_dictionary.md            ← field reference
│   ├── methodology.md                ← model and DAX decisions
│   └── dashboard_walkthrough.md      ← visual-by-visual breakdown
├── images/
│   ├── dashboard_overview.png
│   ├── dashboard_instagram.png
│   └── data_model.png
├── data/
│   ├── audit.py                      ← Python audit script
│   ├── raw/                          ← full source CSVs (400k events)
│   │   ├── README.md
│   │   ├── ad_events.csv
│   │   ├── ads.csv
│   │   ├── campaigns.csv
│   │   └── users.csv
│   └── sample/                       ← clean 2k-row subset
│       ├── README.md
│       └── (4 sample CSVs)
└── dashboard/
    └── README.md
```
