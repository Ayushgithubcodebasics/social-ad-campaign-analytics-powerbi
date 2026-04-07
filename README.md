# Meta Ad Campaign Analytics — Power BI

A Power BI report analyzing Facebook and Instagram ad performance built on a synthetic dataset — 50 campaigns, 200 ads, 9,841 users, 400,000 events spanning May–August 2025.

**[→ Live dashboard](https://app.powerbi.com/view?r=eyJrIjoiMmVhYTNkZTUtYmEzOS00YmYzLWI4MmMtZWI5YjJjZTg0MGI3IiwidCI6ImM2ZTU0OWIzLTVmNDUtNDAzMi1hYWU5LWQ0MjQ0ZGM1YjJjNCJ9)**

The working `.pbix` file is [`meta_ad_performance.pbix`](meta_ad_performance.pbix). Raw source data is in [`data/raw/`](data/raw/).

---

## Numbers at a glance

| Metric | Facebook | Instagram | Combined |
|---|---:|---:|---:|
| Impressions | 215,972 | 123,840 | 339,812 |
| Clicks | 25,389 | 14,690 | 40,079 |
| CTR | 11.76% | 11.86% | 11.79% |
| Engagements | 29,296 | 16,848 | 46,144 |
| Engagement Rate | 13.56% | 13.60% | 13.58% |
| Purchases | 1,323 | 708 | 2,031 |
| Conversion Rate | 5.21% | 4.82% | 5.07% |
| Purchase Rate | 0.61% | 0.57% | 0.60% |

Total budget: $2,535,923.78 across 50 campaigns. Blended CPA: $1,248.61 (campaign-level only — budget isn't split by platform in the source data, so per-platform CPA can't be computed).

Likes (FB: 7,505 / IG: 4,508) are tracked but excluded from Engagements — see [methodology.md](docs/methodology.md) for the full definition.

---

## What the data actually shows

**The funnel drops hard after the click.**

```
215,972 impressions
    ↓ 11.76% CTR
 25,389 clicks
    ↓ 5.21% CVR
  1,323 purchases
```

~24,000 people clicked and left empty-handed. CTR is 6–10× the industry average of 1–2%, so the ads are doing their job. The failure is post-click. A 1 percentage point improvement in Facebook CVR would yield ~254 additional purchases — worth $317,009 without increasing total spend. That's where I'd focus first.

**Platform-specific format strategy is required — a uniform cross-platform approach misallocates budget.** Facebook and Instagram respond to formats differently:

#### Facebook ad formats
| Ad Type | Impressions | CTR | Conv. Rate | Eng. Rate |
|---|---:|---:|---:|---:|
| Stories | 71,537 | 11.75% | **5.52%** | 13.61% |
| Video | 45,770 | **11.88%** | 5.22% | **13.74%** |
| Carousel | 47,752 | 11.73% | 5.05% | 13.44% |
| Image | 50,913 | 11.67% | 4.91% | 13.46% |

#### Instagram ad formats
| Ad Type | Impressions | CTR | Conv. Rate | Eng. Rate |
|---|---:|---:|---:|---:|
| Carousel | 38,921 | 11.70% | **5.23%** | 13.46% |
| Stories | 37,395 | 11.70% | 5.00% | 13.44% |
| Image | 37,251 | **12.17%** | 4.35% | **13.88%** |
| Video | 10,273 | 11.96% | 4.39% | 13.74% |

Note: the CTR differences between formats are narrow (11.43%–12.17% across both platforms, under 1pp spread). This is a synthetic dataset — the CTR variance is too low to draw strong conclusions from format comparisons on that metric alone. The CVR gaps are wider and more meaningful.

- **Facebook:** Lead with Stories (CVR 5.52%, 33% of FB impressions) and Video (CTR 11.88%, ER 13.74%). Less Image.
- **Instagram:** Lead with Carousel for conversion campaigns (CVR 5.23%, beats Stories). Don't import Facebook's "Stories first" logic to Instagram.

**The US dominates volume; Canada and India lead on efficiency; Germany underperforms.** Top countries by Facebook engagement:

| Country | FB Engagements | FB Impressions | CTR | Conv. Rate | Purchases |
|---|---:|---:|---:|---:|---:|
| United States | 8,426 | 61,923 | 11.80% | 5.35% | 391 |
| United Kingdom | 4,127 | 31,335 | 11.43% | 4.94% | 177 |
| Canada | 2,736 | 20,307 | 11.77% | **5.44%** | 130 |
| India | 2,670 | 19,318 | **12.03%** | 5.29% | 123 |
| Germany | 2,373 | 17,043 | 11.83% | 4.86% | 98 |

Canada has the highest CVR (5.44%) and India the highest CTR (12.03%). Germany is last on CVR (4.86%). Reduce Germany, increase India and Canada.

**Target gender vs. actual user gender don't match.** 55.2% of actual Facebook engagers are male. 21.7% of ad targeting is male-targeted. The ads are skewed toward female targeting but the audience engaging is predominantly male. Test male-targeted and all-targeted creative variants.

**Time-of-day patterns are nearly flat — dayparting is not supported by this data.** Combined engagements: Afternoon 11,610 / Evening 11,574 / Morning 11,520 / Night 11,440. Under 1.5% spread. This makes sense for synthetic data — the generator used uniform random timestamps, so there's no real hourly signal to find here. Dayparting optimization isn't supported by these numbers.

---

## Data quality issues found

Three things caught before building any visuals:

1. **User join gap (5.01%)** — 20,046 event rows have no matching user. Root cause: **406 corrupted user IDs** in `users.csv` from two Excel CSV-opening artifacts:
   - **289 IDs in scientific notation** (`50e00` → `5.00E+01`) — Excel silently converts hex IDs containing 'e'. `ad_events.csv` kept the original string; join breaks.
   - **117 IDs with leading zeros stripped** (`00062` → `62`) — Excel treats all-numeric IDs as integers. Same result.
   - These 20,046 events still count in all event KPIs (impressions, clicks, purchases). They're excluded from demographic breakdowns.

2. **Campaign window violations (56.4%)** — 225,406 events fall outside their campaign's start/end dates. Events span May 7 – August 6, 2025; campaign dates span February–October 2025. The mismatch is too large to be a timezone issue — campaign dates aren't reliable event boundaries here.

3. **Budget fanout** — `total_budget` is one row per campaign. Join it down and SUM:

| Aggregation grain | Total | Multiplier |
|---|---:|---:|
| Campaign (correct) | $2,535,923.78 | 1× |
| Joined to ads | $10,222,673.08 | 4× |
| Joined to events | $20,467,767,701.97 | 8,071× |

All budget measures pull directly from the campaigns table.

The Python audit script covering all of this is at [`data/audit.py`](data/audit.py).

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

`ad_events` is the fact table. The calendar table was built in DAX using `CALENDARAUTO()` off a derived `event_date` column — needed for DAX time intelligence to work correctly.

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
│   └── sample/                       ← clean 2k-row subset
└── dashboard/
    └── README.md
```
