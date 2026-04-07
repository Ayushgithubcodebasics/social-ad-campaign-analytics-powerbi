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
| Comments | 2,632 |
| Shares | 1,275 |
| Likes | 7,505 *(tracked; excluded from Engagements — see note below)* |
| Engagements (Clicks + Comments + Shares) | 29,296 |
| Purchases | 1,323 |
| CTR | 11.76% |
| Engagement Rate | 13.56% |
| Conversion Rate | 5.21% |
| Purchase Rate | 0.61% |
| Blended CPA | $1,248.61 *(campaign-level blended; see note below)* |
| Total Budget | $2,535,923.78 |
| Avg Budget per Campaign | $50,718.48 |

### Instagram
| Metric | Value |
|---|---|
| Impressions | 123,840 |
| Clicks | 14,690 |
| Comments | 1,476 |
| Shares | 682 |
| Likes | 4,508 *(tracked; excluded from Engagements)* |
| Engagements (Clicks + Comments + Shares) | 16,848 |
| Purchases | 708 |
| CTR | 11.86% |
| Engagement Rate | 13.60% |
| Conversion Rate | 4.82% |
| Purchase Rate | 0.57% |

### Combined
| Metric | Value |
|---|---|
| Impressions | 339,812 |
| Clicks | 40,079 |
| Comments | 4,108 |
| Shares | 1,957 |
| Likes | 12,013 *(excluded from Engagements)* |
| Engagements | 46,144 |
| Purchases | 2,031 |
| CTR | 11.79% |
| Engagement Rate | 13.58% |
| Conversion Rate | 5.07% |
| Purchase Rate | 0.60% |

> **Note on Engagements:** Likes (FB: 7,505 / IG: 4,508 / Combined: 12,013) are tracked in the source data but deliberately excluded from the Engagements measure. Engagements = Clicks + Comments + Shares — higher-intent interactions only. Most external Meta Ads benchmarks include Likes in "engagement," so direct rate comparisons to industry figures should account for this exclusion.

> **Note on Blended CPA:** `total_budget` is stored at campaign grain and is not split by platform or ad type in the source data. $2,535,923.78 ÷ 2,031 purchases = **$1,248.61 blended CPA**. Platform-level or format-level CPA cannot be computed without a cost allocation in the source.

Facebook has more volume. Instagram has a slightly better CTR but lower conversion rate — more clicks, fewer purchases per click.

---

## What the data actually shows

**The funnel drops hard after the click.** Facebook: 215,972 impressions → 25,389 clicks → 1,323 purchases. That's a 94.8% drop-off between click and purchase. CTR is strong at 11.76% (industry average is 1–2%), so the ads are working. The issue is post-click. A 1 percentage point improvement in Facebook CVR would yield ~254 additional purchases — worth **$317,009** at the blended CPA of $1,248.61 from the same budget. That is the single highest-value lever in the dataset.

**Platform-specific format strategy is required — a uniform cross-platform approach misallocates budget.** Facebook and Instagram respond to formats differently:

#### Facebook ad formats
| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Purchase Rate | Eng. Rate |
|---|---:|---:|---:|---:|---:|---:|
| Stories | 71,537 | 8,406 | 11.75% | **5.52%** | 0.65% | 13.61% |
| Video | 45,770 | 5,438 | **11.88%** | 5.22% | 0.62% | **13.74%** |
| Carousel | 47,752 | 5,602 | 11.73% | 5.05% | 0.59% | 13.44% |
| Image | 50,913 | 5,943 | 11.67% | 4.91% | 0.57% | 13.46% |

On Facebook: **Stories** has the best reach (71,537 impressions — 33% of all FB impressions) and best CVR (5.52%). **Video** leads CTR (11.88%) and engagement rate (13.74%). Image is last or second-to-last on every efficiency metric.

#### Instagram ad formats
| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Purchase Rate | Eng. Rate |
|---|---:|---:|---:|---:|---:|---:|
| Carousel | 38,921 | 4,553 | 11.70% | **5.23%** | 0.61% | 13.46% |
| Stories | 37,395 | 4,376 | 11.70% | 5.00% | 0.59% | 13.44% |
| Image | 37,251 | 4,532 | **12.17%** | 4.35% | 0.53% | **13.88%** |
| Video | 10,273 | 1,229 | 11.96% | 4.39% | 0.53% | 13.74% |

On Instagram: **Carousel** is the top converter at CVR 5.23% — not Stories. **Image** leads CTR (12.17%) but is the worst converter (4.35%). A "run more Stories everywhere" strategy based on Facebook data would reduce Instagram conversions.

**Recommended platform-specific format strategy:**
- **Facebook:** Lead with Stories (CVR 5.52%, 33% of FB impressions) and Video (CTR 11.88%, ER 13.74%)
- **Instagram:** Lead with Carousel (CVR 5.23%) for conversion campaigns; Image (CTR 12.17%) for awareness/reach campaigns

**The US dominates volume; Canada and India lead on efficiency; Germany underperforms.** Top countries by Facebook-only engagement:

| Country | FB Engagements | FB Impressions | Clicks | CTR | Conv. Rate | Purchases |
|---|---:|---:|---:|---:|---:|---:|
| United States | 8,426 | 61,923 | 7,304 | 11.80% | 5.35% | 391 |
| United Kingdom | 4,127 | 31,335 | 3,581 | 11.43% | 4.94% | 177 |
| Canada | 2,736 | 20,307 | 2,391 | 11.77% | **5.44%** | 130 |
| India | 2,670 | 19,318 | 2,324 | **12.03%** | 5.29% | 123 |
| Germany | 2,373 | 17,043 | 2,017 | 11.83% | 4.86% | 98 |

Canada has the highest CVR (5.44%) and India has the highest CTR (12.03%) of the five major markets. Germany has the lowest CVR (4.86%) and second-lowest CTR — the clear underperformer. **Budget reallocation recommendation: reduce Germany, increase India and Canada.** Both outperform Germany on efficiency and would generate more purchases from the same total spend.

**Target gender vs. actual user gender don't match.** Female-targeted ads account for 43.4% of Facebook engagements by targeting allocation. But actual users engaging on Facebook are **55.2% male vs 34.7% female** (Other: 10.1%). The campaign targeting is heavily female, but the engaging audience is predominantly male. Recommended action: test increasing allocation to Male-targeted and All-targeted ad variants, or add male-targeted creative to campaigns currently running female-only targeting.

**Time-of-day patterns are nearly flat — dayparting is not supported by this data.** Combined FB+IG engagements: Afternoon 11,610 / Evening 11,574 / Morning 11,520 / Night 11,440. Under 1.5% spread between peak and trough. Facebook-only is equally flat: Evening 7,382 / Afternoon 7,330 / Morning 7,309 / Night 7,275. Day-of-week: Friday 4,274 (FB peak) to Thursday 4,128 (FB trough) — 3.4% spread. Standard Meta Ads guidance recommends afternoon/evening scheduling and Tuesday–Thursday targeting. **This dataset does not support that recommendation. Dayparting would not meaningfully move the needle here.**

---

## Data quality issues found

Three things caught before building any visuals:

1. **User join gap (5.01%)** — 20,046 event rows have no matching user. Root cause: **406 corrupted user IDs** in `users.csv` from two separate Excel CSV-opening artifacts:
   - **289 IDs in scientific notation** (`1.20E+01`, `5.00E+01`, etc.) — Excel silently converts hex IDs containing 'e' (e.g., `50e00` → `5.00E+01`). The `user_id` values in `ad_events.csv` retained the original string, so the join breaks for those 289 users.
   - **117 IDs with leading zeros stripped** (`00062` → `62`, `00095` → `95`) — Excel treats all-numeric IDs as integers and removes leading zeros on CSV open. `ad_events.csv` retains `00062`; `users.csv` has `62`; join fails.
   - These 20,046 events still count in all event-count KPIs (impressions, clicks, purchases). They are excluded from all demographic breakdowns (gender, age, country, interests). Any user-level analysis has a ~5% coverage gap.

2. **Campaign window violations (56.4%)** — 225,406 events fall outside their campaign's start/end dates. Events span May 7 – August 6, 2025. Campaign dates span February–October 2025. The mismatch is too large to be a timezone artifact — campaign dates are not reliable event boundaries and are not used as analysis filters.

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

Likes exist in the source data but are excluded from Engagements — defined as Clicks + Comments + Shares to capture only higher-intent interactions.

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
