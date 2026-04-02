# Findings

Full dataset: 50 campaigns, 200 ads, 9,841 users, 400,000 events (May 7 – Aug 6, 2025).

---

## Overall KPIs

| Platform | Impressions | Clicks | CTR | Engagements | Eng. Rate | Purchases | Conv. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Facebook | 215,972 | 25,389 | 11.76% | 29,296 | 13.56% | 1,323 | 5.21% | 0.61% |
| Instagram | 123,840 | 14,690 | 11.86% | 16,848 | 13.60% | 708 | 4.82% | 0.57% |
| Combined | 339,812 | 40,079 | 11.79% | 46,144 | 13.58% | 2,031 | 5.07% | 0.60% |

Total budget: $2,535,923.78 across 50 campaigns ($50,718 avg per campaign).

---

## Finding 1: The funnel collapses between click and purchase

On Facebook: 215,972 impressions → 25,389 clicks → 1,323 purchases.

That's 11.76% CTR (strong — industry benchmark is 1–2%), then a 94.8% drop between click and purchase. Nearly 24,000 people clicked on a Facebook ad and didn't buy anything.

Conversion rate from click to purchase is 5.21%. That's not terrible in isolation. The problem is scale — with 25K clicks, even a 1-point improvement in conversion rate would mean ~250 more purchases. That's the lever worth pulling.

The same pattern holds on Instagram: 14,690 clicks, 708 purchases, 4.82% conversion rate. Instagram's CTR is marginally higher (11.86%) but conversion rate is lower. More clicks, fewer conversions per click.

The ads are clearly working at generating interest. Whatever happens after the click — the landing page, the offer, the checkout — that's where revenue is being left on the table.

---

## Finding 2: Stories wins on volume, Video is the efficiency standout

Facebook ad type breakdown:

| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Eng. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|
| Stories | 71,537 | 8,406 | 11.75% | **5.52%** | 13.61% | **0.65%** |
| Video | 45,770 | 5,438 | **11.88%** | 5.22% | **13.74%** | 0.62% |
| Carousel | 47,752 | 5,602 | 11.73% | 5.05% | 13.44% | 0.59% |
| Image | 50,913 | 5,943 | 11.67% | 4.91% | 13.46% | 0.57% |

Stories gets the most reach (71,537 impressions — 33% of all Facebook impressions) and the best conversion rate (5.52%). Video has the highest CTR (11.88%), highest engagement rate (13.74%), but a smaller audience and second-best conversion rate.

Image and Carousel both trail on conversion rate and engagement. Image gets decent reach (50,913) but is the worst converter at 4.91%. It's essentially dead weight at the bottom of the format ranking.

If you're trying to maximize purchases per impression, you'd go Stories. If you're trying to maximize engagement per impression, you'd go Video. Neither is a wrong answer — depends whether you're optimizing for reach or efficiency.

On Instagram, the format rankings shift: Image jumps to the highest CTR (12.17%), and Stories' conversion rate drops to 5.00%. The Instagram audience responds differently to formats than Facebook — so the format strategy probably shouldn't be uniform across platforms.

---

## Finding 3: The US drives volume, Canada drives conversions, India drives CTR

Top countries by Facebook engagement:

| Country | Engagements | Impressions | Clicks | CTR | Conv. Rate | Purchases |
|---|---:|---:|---:|---:|---:|---:|
| United States | 13,279 | 61,923 | 7,304 | 11.80% | 5.35% | 391 |
| United Kingdom | 6,572 | 31,335 | 3,581 | 11.43% | 4.94% | 177 |
| Canada | 4,345 | 20,307 | 2,391 | 11.77% | 5.44% | 130 |
| India | 4,170 | 19,318 | 2,324 | 12.03% | 5.29% | 123 |
| Germany | 3,695 | 17,043 | 2,017 | 11.83% | 4.86% | 98 |

The US dominates on raw numbers — 391 purchases, 13,279 engagements, 61,923 impressions. It's not close. India and Brazil get cited in a lot of "high engagement market" narratives, but in this dataset, the US is the actual volume story.

A few things worth calling out:
- India has the highest CTR (12.03%) of any major market. People are clicking more, and conversion rate is solid at 5.29%. Worth more investment than it's currently getting relative to the US.
- Canada has the highest conversion rate (5.44%). Fewer impressions than the US but a higher percentage of clicks turning into purchases. Budget efficiency is better here than the headline numbers suggest.
- UK has the lowest CTR (11.43%) of the five biggest markets. Impressions are high but interest is lower per view.
- Germany's conversion rate (4.86%) is the weakest of the major markets. Impressions and clicks but not converting well.

A flat global budget doesn't account for these differences. India and Canada are outperforming their budget allocation on efficiency metrics.

---

## Finding 4: The targeting-vs-reality gender gap

Female-targeted ads account for 43.4% of Facebook engagements (based on what the ads were set to target). Male-targeted is 21.7%.

But when you look at who's actually clicking — the real user gender from the users table — males make up 54.4% of Facebook engagers, females 34.2%.

That's a meaningful discrepancy. The campaign strategy is heavily tilted toward female targeting, but male users are the ones doing most of the engaging. Either the female targeting isn't as effective as assumed, or male users are engaging with female-targeted ads (which would be a targeting inefficiency). Either way, this is worth investigating before allocating more budget to female-targeted content.

---

## Finding 5: Time-of-day patterns are nearly flat

| Time Segment | Engagements |
|---|---|
| Afternoon | 11,610 |
| Evening | 11,574 |
| Morning | 11,520 |
| Night | 11,440 |

1.5% spread between the peak (Afternoon) and the trough (Night). Day-of-week is just as flat — Friday leads at 6,698, Thursday is last at 6,510, less than 3% difference.

The "schedule ads in the afternoon/evening" recommendation shows up in almost every Meta Ads analysis. In this specific dataset, it's not supported by the numbers. All four time segments are within noise range of each other. Dayparting probably won't move the needle here.

---

## Finding 6: Campaign_32_Summer is the anomaly worth examining

Campaign_32_Summer has a 12.57% CTR — the third highest of any campaign. But its conversion rate is 0.93%. That means 99 out of every 100 clickers left without buying. While the average campaign converts 5%+ of its clicks, this one converts less than 1%.

That's not a targeting problem (people are clearly clicking). Something breaks at the next step. The landing page, the offer, the checkout flow — one of those is failing badly for this specific campaign. Most other campaigns are in the 4–8% conversion range. This one is 6× worse than the worst comparable.

Best converting campaigns for reference: Campaign_14_Summer (8.33% CVR), Campaign_27_Q3 (7.54% CVR). Both have lower CTR than Campaign_32_Summer but far better post-click performance.

---

## Recommendations

1. **Focus on the post-click experience.** The ads are getting clicks. 94.8% of those clicks don't convert. That's where the money is being lost, and it won't be fixed by changing ad creative or targeting.

2. **Shift budget toward Stories and Video on Facebook.** Stories has the best reach-to-purchase ratio. Video has the best engagement efficiency. Image and Carousel are underperforming on every efficiency metric.

3. **Invest more in India and Canada relative to spend.** India has the highest CTR of any major market. Canada has the highest conversion rate. Both are being outspent by the US, which has more volume but not necessarily better efficiency.

4. **Don't optimize for gender targeting based on current assumptions.** Male users are engaging significantly more than female-targeting allocation would predict. The targeting strategy may be misaligned with actual audience behavior.

5. **Investigate Campaign_32_Summer separately.** A 0.93% conversion rate with 12.57% CTR is a specific failure in the post-click funnel for that campaign, not a general problem. That campaign needs its landing page and offer audited independently.
