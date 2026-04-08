-- =============================================================================
-- analysis.sql — Meta Ad Campaign Analytics
-- SQL validation and analysis layer for the Power BI dashboard findings.
--
-- These queries run against the raw CSV data loaded into SQLite.
-- To set up: python data/load_to_sqlite.py  (creates ad_analysis.db)
-- Tables: ad_events, ads, campaigns, users
--
-- Key techniques: CTE, window functions (RANK, ROW_NUMBER, SUM OVER),
--                 CASE WHEN, subqueries, multi-table JOINs
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Q1. Full funnel by platform — validates the Power BI headline KPIs
-- Answers: What is the end-to-end conversion funnel for Facebook vs Instagram?
-- Cross-checks the dashboard figures (FB CTR 11.76%, CVR 5.21% etc.)
-- -----------------------------------------------------------------------------

WITH funnel AS (
    SELECT
        a.ad_platform,
        COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS Impressions,
        COUNT(CASE WHEN e.event_type = 'Click'      THEN 1 END) AS Clicks,
        COUNT(CASE WHEN e.event_type = 'Comment'    THEN 1 END) AS Comments,
        COUNT(CASE WHEN e.event_type = 'Share'      THEN 1 END) AS Shares,
        COUNT(CASE WHEN e.event_type = 'Like'       THEN 1 END) AS Likes,
        COUNT(CASE WHEN e.event_type = 'Purchase'   THEN 1 END) AS Purchases
    FROM ad_events e
    JOIN ads a ON e.ad_id = a.ad_id
    GROUP BY a.ad_platform
)
SELECT
    ad_platform                                             AS Platform,
    Impressions,
    Clicks,
    Purchases,
    -- Engagements excludes Likes (deliberate — see methodology.md)
    Clicks + Comments + Shares                              AS Engagements,
    ROUND(Clicks     * 100.0 / NULLIF(Impressions, 0), 2)  AS CTR_Pct,
    ROUND(Purchases  * 100.0 / NULLIF(Clicks, 0), 2)       AS CVR_Pct,
    ROUND((Clicks + Comments + Shares) * 100.0
          / NULLIF(Impressions, 0), 2)                      AS EngagementRate_Pct,
    ROUND(Purchases  * 100.0 / NULLIF(Impressions, 0), 2)  AS PurchaseRate_Pct
FROM funnel
ORDER BY Impressions DESC;


-- -----------------------------------------------------------------------------
-- Q2. Ad format performance by platform — CVR ranked
-- Answers: Which format should each platform prioritise for conversions?
-- Surfaces the Stories vs Carousel insight from Finding 2.
-- -----------------------------------------------------------------------------

WITH format_stats AS (
    SELECT
        a.ad_platform,
        a.ad_type,
        COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS Impressions,
        COUNT(CASE WHEN e.event_type = 'Click'      THEN 1 END) AS Clicks,
        COUNT(CASE WHEN e.event_type = 'Purchase'   THEN 1 END) AS Purchases
    FROM ad_events e
    JOIN ads a ON e.ad_id = a.ad_id
    GROUP BY a.ad_platform, a.ad_type
)
SELECT
    ad_platform                                             AS Platform,
    ad_type                                                 AS Format,
    Impressions,
    Clicks,
    Purchases,
    ROUND(Clicks    * 100.0 / NULLIF(Impressions, 0), 2)   AS CTR_Pct,
    ROUND(Purchases * 100.0 / NULLIF(Clicks, 0), 2)        AS CVR_Pct,
    -- Rank CVR within each platform to surface the best format per platform
    RANK() OVER (
        PARTITION BY ad_platform
        ORDER BY CAST(Purchases AS REAL) / NULLIF(Clicks, 0) DESC
    )                                                        AS CVR_Rank_Within_Platform
FROM format_stats
ORDER BY ad_platform, CVR_Rank_Within_Platform;


-- -----------------------------------------------------------------------------
-- Q3. Campaign performance ranked — identifying outliers
-- Answers: Which campaigns are the most and least efficient converters?
-- Campaign_32_Summer (12.57% CTR, 0.93% CVR) should rank worst on CVR
-- while having a high CTR — the clearest signal of a post-click problem.
-- -----------------------------------------------------------------------------

WITH campaign_stats AS (
    SELECT
        c.name                                                   AS CampaignName,
        COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS Impressions,
        COUNT(CASE WHEN e.event_type = 'Click'      THEN 1 END) AS Clicks,
        COUNT(CASE WHEN e.event_type = 'Purchase'   THEN 1 END) AS Purchases,
        ROUND(c.total_budget, 2)                                 AS Budget
    FROM ad_events e
    JOIN ads a      ON e.ad_id      = a.ad_id
    JOIN campaigns c ON a.campaign_id = c.campaign_id
    GROUP BY c.campaign_id, c.name, c.total_budget
    HAVING Clicks > 0
)
SELECT
    CampaignName,
    Impressions,
    Clicks,
    Purchases,
    Budget,
    ROUND(Clicks    * 100.0 / NULLIF(Impressions, 0), 2)  AS CTR_Pct,
    ROUND(Purchases * 100.0 / NULLIF(Clicks, 0), 2)       AS CVR_Pct,
    -- Cost per acquisition at campaign level
    ROUND(Budget / NULLIF(Purchases, 0), 2)               AS CPA,
    RANK() OVER (ORDER BY CAST(Purchases AS REAL) / NULLIF(Clicks, 0) ASC) AS WorstCVR_Rank,
    RANK() OVER (ORDER BY CAST(Purchases AS REAL) / NULLIF(Clicks, 0) DESC) AS BestCVR_Rank
FROM campaign_stats
ORDER BY CVR_Pct ASC;


-- -----------------------------------------------------------------------------
-- Q4. Geo performance — CTR and CVR by user country
-- Answers: Which markets are most efficient? Validates the Germany vs Canada
-- and India comparison from Finding 3.
-- Joins to users table — note the 5.01% join gap from corrupted user IDs
-- (see data quality documentation). Results reflect the 94.99% matched events.
-- -----------------------------------------------------------------------------

WITH geo_stats AS (
    SELECT
        u.country,
        a.ad_platform,
        COUNT(CASE WHEN e.event_type = 'Impression' THEN 1 END) AS Impressions,
        COUNT(CASE WHEN e.event_type = 'Click'      THEN 1 END) AS Clicks,
        COUNT(CASE WHEN e.event_type = 'Purchase'   THEN 1 END) AS Purchases
    FROM ad_events e
    JOIN ads  a ON e.ad_id  = a.ad_id
    JOIN users u ON e.user_id = u.user_id   -- 5.01% of events have no user match
    WHERE a.ad_platform = 'Facebook'
    GROUP BY u.country, a.ad_platform
    HAVING Impressions > 5000   -- exclude negligible markets
)
SELECT
    country,
    Impressions,
    Clicks,
    Purchases,
    ROUND(Clicks    * 100.0 / NULLIF(Impressions, 0), 2) AS CTR_Pct,
    ROUND(Purchases * 100.0 / NULLIF(Clicks, 0), 2)      AS CVR_Pct,
    RANK() OVER (ORDER BY CAST(Purchases AS REAL) / NULLIF(Clicks, 0) DESC) AS CVR_Rank
FROM geo_stats
ORDER BY Impressions DESC;


-- -----------------------------------------------------------------------------
-- Q5. Gender targeting vs actual user gender — quantifying the inversion
-- Answers: How large is the gap between who the ads target and who engages?
-- 55.2% of actual engagers are male vs 21.7% male-targeted ads (Finding 4).
-- -----------------------------------------------------------------------------

-- Targeting distribution (from ads table — what was planned)
SELECT
    'Ad targeting distribution' AS Source,
    target_gender               AS Gender,
    COUNT(*)                    AS AdCount,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS SharePct
FROM ads
GROUP BY target_gender

UNION ALL

-- Actual engager distribution (from users table — what happened)
SELECT
    'Actual engager distribution' AS Source,
    u.user_gender                 AS Gender,
    COUNT(DISTINCT e.user_id)     AS UserCount,
    ROUND(COUNT(DISTINCT e.user_id) * 100.0
          / SUM(COUNT(DISTINCT e.user_id)) OVER (), 1) AS SharePct
FROM ad_events e
JOIN users u ON e.user_id = u.user_id
WHERE e.event_type = 'Click'
GROUP BY u.user_gender

ORDER BY Source, SharePct DESC;
