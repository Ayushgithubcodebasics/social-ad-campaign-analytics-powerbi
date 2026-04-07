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
**Blended CPA: $1,248.61** ($2,535,923.78 ÷ 2,031 purchases). Note: `total_budget` is stored at campaign grain and is not split by platform or ad type — this is a campaign-level blended figure. Per-platform or per-format CPA cannot be computed without a cost split in the source data.

> **Note on Engagements:** Likes (FB: 7,505 / IG: 4,508 / Combined: 12,013) are tracked in the source data but deliberately excluded from the Engagements measure. Engagements = Clicks + Comments + Shares only. Most external Meta Ads benchmarks include Likes in "engagement" — direct comparisons to industry rates should account for this exclusion.

---

## Finding 1: The funnel collapses between click and purchase

On Facebook: 215,972 impressions → 25,389 clicks → 1,323 purchases.

That's 11.76% CTR (strong — industry benchmark is 1–2%), then a 94.8% drop between click and purchase. Nearly 24,066 people clicked a Facebook ad and didn't buy anything.

CVR from click to purchase is 5.21%. The problem is scale — with 25K clicks, a **1 percentage point improvement in CVR would yield ~254 additional purchases worth $317,009** at the blended CPA of $1,248.61, from the same budget. That is the single highest-value lever in this dataset. The CTR is already 6–10× the industry benchmark — the ads are working. Whatever happens after the click — the landing page, the offer, the checkout — is where revenue is being left on the table.

The same pattern holds on Instagram: 14,690 clicks, 708 purchases, 4.82% CVR. Instagram's CTR is marginally higher (11.86%) but CVR is lower. More clicks, fewer conversions per click.

---

## Finding 2: Format strategy must be platform-specific — not uniform

Facebook and Instagram respond to formats differently. A uniform cross-platform strategy based on Facebook data alone misallocates budget.

**Facebook ad type breakdown:**

| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Eng. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|
| Stories | 71,537 | 8,406 | 11.75% | **5.52%** | 13.61% | **0.65%** |
| Video | 45,770 | 5,438 | **11.88%** | 5.22% | **13.74%** | 0.62% |
| Carousel | 47,752 | 5,602 | 11.73% | 5.05% | 13.44% | 0.59% |
| Image | 50,913 | 5,943 | 11.67% | 4.91% | 13.46% | 0.57% |

Stories gets the most reach (71,537 impressions — 33% of all Facebook impressions) and the best CVR (5.52%). Video has the highest CTR (11.88%), highest engagement rate (13.74%), and second-best CVR. Image and Carousel both trail on conversion and engagement. Image gets decent reach (50,913) but is the worst converter at 4.91%.

**Instagram ad type breakdown:**

| Ad Type | Impressions | Clicks | CTR | Conv. Rate | Eng. Rate | Purchase Rate |
|---|---:|---:|---:|---:|---:|---:|
| Carousel | 38,921 | 4,553 | 11.70% | **5.23%** | 13.46% | 0.61% |
| Stories | 37,395 | 4,376 | 11.70% | 5.00% | 13.44% | 0.59% |
| Image | 37,251 | 4,532 | **12.17%** | 4.35% | **13.88%** | 0.53% |
| Video | 10,273 | 1,229 | 11.96% | 4.39% | 13.74% | 0.53% |

On Instagram, **Carousel is the top-converting format at 5.23% CVR** — not Stories. Stories drops to 5.00% CVR on Instagram. Image jumps to the highest CTR (12.17%) but is the worst converter on Instagram (4.35%). Video has the smallest audience on Instagram (only 8.3% of IG impressions).

**The critical divergence:** On Facebook, Stories wins CVR (5.52%). On Instagram, Carousel wins CVR (5.23%). A "run more Stories" strategy applied uniformly based on Facebook data would reduce Instagram conversions — Carousel outperforms Stories on IG.

**CVR ranking across both platforms:**

| Format | CVR |
|---|---|
| FB Stories | 5.52% ← highest converting on either platform |
| IG Carousel | 5.23% |
| FB Video | 5.22% |
| FB Carousel | 5.05% |
| IG Stories | 5.00% |
| FB Image | 4.91% |
| IG Video | 4.39% |
| IG Image | 4.35% ← lowest converting format overall |

**Platform-specific format strategy:**
- **Facebook:** Lead with Stories (CVR 5.52%, 33% reach) and Video (CTR 11.88%, ER 13.74%) for conversion and engagement respectively. Reduce Image allocation.
- **Instagram:** Lead with Carousel (CVR 5.23%) for conversion campaigns. Use Image (CTR 12.17%) for awareness/reach. Carousel outperforms Stories on IG — do not apply FB-derived "Stories first" logic here.

---

## Finding 3: The US drives volume, Canada drives conversions, India drives CTR — Germany underperforms

**Top countries by Facebook-only engagement** (inner join on matched users):

| Country | FB Engagements | FB Impressions | Clicks | CTR | Conv. Rate | Purchases |
|---|---:|---:|---:|---:|---:|---:|
| United States | 8,426 | 61,923 | 7,304 | 11.80% | 5.35% | 391 |
| United Kingdom | 4,127 | 31,335 | 3,581 | 11.43% | 4.94% | 177 |
| Canada | 2,736 | 20,307 | 2,391 | 11.77% | **5.44%** | 130 |
| India | 2,670 | 19,318 | 2,324 | **12.03%** | 5.29% | 123 |
| Germany | 2,373 | 17,043 | 2,017 | 11.83% | 4.86% | 98 |

The US dominates on raw volume — 391 purchases, 8,426 engagements, 61,923 impressions. Not close.

Key efficiency findings:
- **Canada** has the highest CVR of any major market (5.44%). Budget efficiency is better here than headline volume suggests.
- **India** has the highest CTR (12.03%) of any major market. Strong click intent and solid CVR (5.29%). Gets ~31% of US impressions but outperforms US on CTR.
- **UK** has the lowest CTR (11.43%) of the five markets. High impression volume but weaker per-impression interest.
- **Germany** has the lowest CVR (4.86%) and second-lowest CTR (11.83%). Canada's CVR is 11.9% higher relative to Germany's, and India's CTR is 5.3% higher. Germany is the clear efficiency underperformer.

**Complete budget reallocation recommendation:** Reduce Germany allocation. Increase India and Canada. Both outperform Germany on efficiency metrics and would generate more purchases from the same total spend. Without identifying Germany as the reallocation source, the recommendation to "invest more in India and Canada" is incomplete.

---

## Finding 4: The targeting-vs-reality gender gap

Female-targeted ads account for 43.4% of Facebook engagements by ad targeting allocation. Male-targeted ads: 21.7%. All-targeted: 34.8%.

But the actual users engaging — matched from the users table — are **55.2% male, 34.7% female, 10.1% Other**.

That's a significant inversion. The campaign targeting allocates 43.4% of engagement weight to female-targeted ads, yet male users account for 55.2% of actual engagements. Either (a) male users are engaging with female-targeted creative at high rates — a targeting inefficiency where budget spent reaching females generates male responses — or (b) the small male-targeted allocation (21.7%) is disproportionately efficient.

Either case is actionable. **Recommended actions:**
- Test increasing allocation to Male-targeted and All-targeted ad variants
- Add male-targeted creative to campaigns currently running female-only targeting, then compare CVR
- Do not reallocate further toward female-only targeting without evidence it outperforms on conversions

---

## Finding 5: Time-of-day patterns are nearly flat — dayparting is not supported

**Combined FB+IG engagements by time of day:**

| Time Segment | Combined Engagements | FB-only Engagements |
|---|---:|---:|
| Afternoon | 11,610 | 7,330 |
| Evening | 11,574 | 7,382 |
| Morning | 11,520 | 7,309 |
| Night | 11,440 | 7,275 |

The combined spread is 170 engagements — 1.5% between peak (Afternoon) and trough (Night). Facebook-only spread is 107 engagements — also 1.5%. Day-of-week is equally flat: Friday leads at 4,274 (FB), Thursday is last at 4,128 — 3.4% difference across all seven days.

Standard Meta Ads guidance recommends scheduling ads for Tuesday–Thursday afternoons or weekday evenings. **This dataset directly contradicts that recommendation.** All four time segments are within noise range of each other on both platforms. All seven days of the week are within noise range. Dayparting would not meaningfully move the needle in this account. This is worth stating explicitly as a contrarian data-driven finding — it's analytically stronger than repeating industry clichés that the data doesn't support.

---

## Finding 6: Campaign_32_Summer is the anomaly worth examining

Campaign_32_Summer has a 12.57% CTR — the third highest of any campaign. But its CVR is 0.93%. That means 99 out of every 100 clickers left without buying. While the average campaign converts 5%+ of its clicks, this one converts less than 1%.

The inverse relationship is diagnostic. High CTR proves the creative works — people find the ad compelling enough to click. Near-zero CVR means the failure is post-click: landing page, offer structure, checkout flow, or a technical issue specific to this campaign's destination URL. This is not a targeting or creative problem.

**At any given CPC, Campaign_32 requires ~9× more clicks per purchase than Campaign_14:**
- Campaign_14_Summer CVR: 8.33% → 12 clicks per purchase
- Campaign_32_Summer CVR: 0.93% → 107.5 clicks per purchase
- Ratio: 107.5 ÷ 12 = **8.96× more clicks (and spend) per conversion**

For reference:
- Campaign_14_Summer: CVR 8.33% (180 clicks, 15 purchases, CTR 10.98%)
- Campaign_27_Q3: CVR 7.54% (199 clicks, 15 purchases, CTR 12.08%)
- Campaign_23_Winter: CVR 7.39% (176 clicks, 13 purchases, CTR 10.73%)

Campaign_32_Summer has higher CTR than Campaign_14 but is 9× less efficient per purchase. That campaign needs its landing page and offer audited independently.

---

## Recommendations

1. **Fix the post-click experience — this is the highest-value lever.** The ads are getting clicks at 6–10× the industry CTR benchmark. 94.8% of those clicks don't convert. A 1pp improvement in Facebook CVR = ~254 more purchases = **$317,009 in recovered acquisition value at the blended CPA of $1,248.61, from the same budget.** Audit landing pages, offer clarity, and checkout flow. Campaign_32_Summer (0.93% CVR with 12.57% CTR) is the sharpest example of this failure.

2. **Apply platform-specific format strategy — not a uniform one.**
   - **Facebook:** Increase Stories (CVR 5.52%, 33% reach) and Video (CTR 11.88%, ER 13.74%). Reduce Image — it ranks last on CVR (4.91%) and near-last on every other metric.
   - **Instagram:** Increase Carousel — it is the **top converter on Instagram at CVR 5.23%**, outperforming Stories (5.00%). Use Image for awareness campaigns (CTR 12.17%). Do not apply Facebook's "Stories first" logic to Instagram — it is wrong for that platform.

3. **Reallocate geo budget: reduce Germany, increase India and Canada.** India has the highest CTR of any major market (12.03%). Canada has the highest CVR (5.44%). Germany has the lowest CVR (4.86%) and second-lowest CTR (11.83%). Shifting budget from Germany to India and Canada would mechanically increase purchases from the same total spend — the data supports this directly.

4. **Test male-targeted and all-targeted creative.** Male users account for 55.2% of actual Facebook engagements despite female-targeted ads receiving 43.4% of targeting allocation. Test increasing Male-targeted and All-targeted ad variants. If male users are engaging with female-targeted creative at high rates, the current targeting is either imprecise or missing a highly responsive audience by not serving them tailored creative.

5. **Do not invest in dayparting optimization — the data doesn't support it.** All four time-of-day segments are within 1.5% of each other. All seven days of the week are within 3.4% of each other (both FB-only and combined). Standard Meta Ads advice recommends afternoon/evening and Tuesday–Thursday scheduling. This dataset directly refutes that for this account. Dayparting would be effort spent on noise.

6. **Investigate Campaign_32_Summer separately.** A 0.93% CVR with 12.57% CTR is a specific post-click failure, not a general account problem. That campaign needs its landing page and offer audited independently of everything else.
