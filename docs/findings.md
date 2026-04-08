# Findings

Full dataset: 50 campaigns, 200 ads, 9,841 users, 400,000 events (May 7 – Aug 6, 2025).

Likes (FB: 7,505 / IG: 4,508) are excluded from Engagements — see [methodology.md](methodology.md) for the full definition.

---

## Overall KPIs

| Platform | Impressions | Clicks | CTR | Engagements | Eng. Rate | Purchases | Conv. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Facebook | 215,972 | 25,389 | 11.76% | 29,296 | 13.56% | 1,323 | 5.21% | 0.61% |
| Instagram | 123,840 | 14,690 | 11.86% | 16,848 | 13.60% | 708 | 4.82% | 0.57% |
| Combined | 339,812 | 40,079 | 11.79% | 46,144 | 13.58% | 2,031 | 5.07% | 0.60% |

Total budget: $2,535,923.78 across 50 campaigns ($50,718 avg per campaign). **Blended CPA: $1,248.61** ($2,535,923.78 ÷ 2,031 purchases). Note: `total_budget` is stored at campaign grain — per-platform or per-format CPA can't be computed without a cost split in the source data.

---

## The funnel drops after the click

```
215,972 impressions
    ↓ 11.76% CTR
 25,389 clicks
    ↓ 5.21% CVR
  1,323 purchases

~24,000 people clicked and left empty-handed.
```

CTR is 11.76% — industry benchmark is 1–2%. The ads are working. The problem is that 94.8% of people who click don't convert.

With 25K clicks, a 1 percentage point improvement in CVR yields ~254 additional purchases worth $317,009 at the blended CPA of $1,248.61, from the same budget. That's where I'd focus first — not the ads, but whatever happens after the click. Landing page, offer, checkout flow. Campaign_32_Summer (0.93% CVR with 12.57% CTR) is the sharpest example of this: the creative clearly works, the destination clearly doesn't.

Instagram follows the same pattern: 14,690 clicks, 708 purchases, 4.82% CVR. Slightly higher CTR than Facebook, lower CVR.

---

## Format strategy has to be platform-specific

Facebook and Instagram respond to formats differently. Applying Facebook's format winners to Instagram misallocates budget.

**Facebook:**

| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Eng. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|
| Stories | 71,537 | 8,406 | 11.75% | **5.52%** | 13.61% | **0.65%** |
| Video | 45,770 | 5,438 | **11.88%** | 5.22% | **13.74%** | 0.62% |
| Carousel | 47,752 | 5,602 | 11.73% | 5.05% | 13.44% | 0.59% |
| Image | 50,913 | 5,943 | 11.67% | 4.91% | 13.46% | 0.57% |

Stories gets the most reach (33% of all Facebook impressions) and the best CVR (5.52%). Video leads on CTR and engagement rate. Image gets decent reach but trails on every efficiency metric.

**Instagram:**

| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Eng. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|
| Carousel | 38,921 | 4,553 | 11.70% | **5.23%** | 13.46% | 0.61% |
| Stories | 37,395 | 4,376 | 11.70% | 5.00% | 13.44% | 0.59% |
| Image | 37,251 | 4,532 | **12.17%** | 4.35% | **13.88%** | 0.53% |
| Video | 10,273 | 1,229 | 11.96% | 4.39% | 13.74% | 0.53% |

On Instagram, Carousel is the top converter at 5.23% CVR — not Stories. Image leads CTR at 12.17% but is the worst converter (4.35%). Video barely registers (8.3% of IG impressions).

One caveat worth noting: CTR differences across all formats on both platforms are within a 0.74pp range (11.43%–12.17%). This is a synthetic dataset, and the CTR variance is too low to draw strong format conclusions on that metric specifically. The CVR gaps are larger and more meaningful for budget decisions.

**Full CVR ranking across platforms:**

| Format | CVR |
|---|---|
| FB Stories | 5.52% ← best converting |
| IG Carousel | 5.23% |
| FB Video | 5.22% |
| FB Carousel | 5.05% |
| IG Stories | 5.00% |
| FB Image | 4.91% |
| IG Video | 4.39% |
| IG Image | 4.35% ← worst converting |

---

## Geo: US drives volume, Canada and India lead efficiency, Germany underperforms

**Top countries by Facebook engagement:**

| Country | FB Engagements | FB Impressions | Clicks | CTR | Conv. Rate | Purchases |
|---|---:|---:|---:|---:|---:|---:|
| United States | 8,426 | 61,923 | 7,304 | 11.80% | 5.35% | 391 |
| United Kingdom | 4,127 | 31,335 | 3,581 | 11.43% | 4.94% | 177 |
| Canada | 2,736 | 20,307 | 2,391 | 11.77% | **5.44%** | 130 |
| India | 2,670 | 19,318 | 2,324 | **12.03%** | 5.29% | 123 |
| Germany | 2,373 | 17,043 | 2,017 | 11.83% | 4.86% | 98 |

US is the volume leader — 391 purchases, not close. But on efficiency, Canada has the highest CVR (5.44%) and India has the highest CTR (12.03%) of any major market. Germany has the lowest CVR (4.86%) and second-lowest CTR. It's the clear underperformer.

Budget reallocation from Germany toward India and Canada would mechanically increase purchases without identifying a new audience — the data supports that directly.

---

## The targeting-vs-reality gender gap

Female-targeted ads account for 43.4% of Facebook engagements by ad targeting. Male-targeted: 21.7%. All-targeted: 34.8%.

Actual users engaging: **55.2% male, 34.7% female, 10.1% Other**.

That's a real inversion. The campaign targeting is weighted toward female audiences, but the people actually engaging are mostly male. Either male users are engaging with female-targeted creative at unusually high rates (a targeting inefficiency), or the small male-targeted allocation is disproportionately efficient. Either way it's something to investigate.

---

## Dayparting isn't supported here

**Combined engagements by time of day:**

| Time Segment | Combined Engagements | FB-only |
|---|---:|---:|
| Afternoon | 11,610 | 7,330 |
| Evening | 11,574 | 7,382 |
| Morning | 11,520 | 7,309 |
| Night | 11,440 | 7,275 |

170 engagements separate peak from trough — 1.5%. Day-of-week is equally flat: Friday leads at 4,274 (FB), Thursday last at 4,128, 3.4% across all seven days.

Standard Meta Ads guidance recommends afternoon/evening and Tuesday–Thursday scheduling. This dataset doesn't support that. The flatness is expected — the synthetic data uses uniform random timestamps, so there's no real hourly signal to find. Dayparting would be effort spent on noise.

---

## Campaign_32_Summer is worth investigating separately

Campaign_32_Summer: 12.57% CTR, 0.93% CVR. That means 99 out of every 100 clickers left without buying.

For comparison:
- Campaign_14_Summer: CVR 8.33% → 12 clicks per purchase
- Campaign_32_Summer: CVR 0.93% → 107.5 clicks per purchase

That's ~9× more spend per conversion. High CTR proves the creative works. Near-zero CVR means the failure is post-click — landing page, offer, or checkout. Not a targeting or creative problem.

---

## Recommendations

**1. Fix the post-click experience first** *(for: Performance Marketing / Landing Page team)*  
The ads are getting clicks at 6–10× the industry CTR benchmark. The issue is what happens after the click. A 1pp improvement in Facebook CVR = ~254 more purchases = **$317,009 in recovered value at the blended CPA, from the same budget**. Start with Campaign_32_Summer — it's the clearest example: 12.57% CTR, 0.93% CVR. Audit the landing page and offer independently; this is not a creative problem.

**2. Run platform-specific format strategies** *(for: Media Planning / Creative Strategy team)*  
A uniform cross-platform format approach misallocates budget. Facebook and Instagram respond to formats differently:
- **Facebook:** prioritise Stories (best CVR at 5.52%, 33% of FB impressions) and Video (best CTR 11.88% + ER 13.74%). Reduce Image allocation — it ranks last on CVR (4.91%).
- **Instagram:** prioritise Carousel for conversion campaigns (5.23% CVR, beats Stories). Use Image for awareness objectives (CTR 12.17%). Do not import Facebook's "Stories first" logic to Instagram.

**3. Shift geo budget from Germany to India and Canada** *(for: Campaign Operations / Geo-targeting team)*  
Germany is the clear underperformer: lowest CVR (4.86%) and second-lowest CTR of the five major markets. Canada has the highest CVR (5.44%) and India the highest CTR (12.03%). Reallocating Germany's budget to these two markets produces more purchases without identifying a new audience.

**4. Test male-targeted creative** *(for: Creative Strategy / Audience team)*  
55.2% of actual Facebook engagers are male. Only 21.7% of ad targeting is male-directed. This inversion suggests either male users are engaging with female-targeted creative at unusually high rates (a targeting inefficiency) or the small male-targeted allocation is disproportionately efficient. Either way: add male-targeted variants to the three largest female-only campaigns, run for 2 weeks, compare CVR.

**5. Deprioritise dayparting optimisation** *(for: Campaign Operations team)*  
The data does not support it. All time-of-day segments are within 1.5% of each other (Afternoon 11,610 vs Night 11,440 engagements). All seven weekdays are within 3.4% of each other. Budget allocated to scheduling optimisation would produce noise, not signal. Redirect that effort to the post-click experience (Recommendation 1).

**6. Commission a standalone audit of Campaign_32_Summer** *(for: Performance Marketing team)*  
12.57% CTR, 0.93% CVR. That is 107 clicks per purchase, vs. 12 clicks per purchase for Campaign_14_Summer. The creative clearly works — the destination clearly does not. Audit the landing page, offer, and checkout flow independently before the next campaign flight.
