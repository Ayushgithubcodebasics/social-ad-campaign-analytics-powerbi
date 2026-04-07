"""
audit.py
--------
Data quality and join coverage audit for the Meta Ad Campaign dataset.

Usage:
    python data/audit.py              # auto-detects raw/ or sample/
    python data/audit.py --raw        # force full dataset (data/raw/)
    python data/audit.py --sample     # force sample dataset (data/sample/)

Run from the repo root. The script auto-detects the full raw data in
data/raw/ and falls back to data/sample/ if raw files aren't present.

Full source results (400k events) are shown in comments throughout.
"""

import pandas as pd
import numpy as np
import os
import sys
import argparse
import warnings
warnings.filterwarnings("ignore")

# ── Argument parsing ──────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Meta Ad Campaign data audit")
group  = parser.add_mutually_exclusive_group()
group.add_argument("--raw",    action="store_true", help="Use full raw dataset")
group.add_argument("--sample", action="store_true", help="Use sample dataset")
args = parser.parse_args()

BASE        = os.path.dirname(os.path.abspath(__file__))
RAW_DIR     = os.path.join(BASE, "raw")
SAMPLE_DIR  = os.path.join(BASE, "sample")

def has_raw():
    return os.path.exists(os.path.join(RAW_DIR, "ad_events.csv"))

if args.raw:
    DATA_DIR  = RAW_DIR
    DATA_LABEL = "FULL (raw)"
elif args.sample:
    DATA_DIR  = SAMPLE_DIR
    DATA_LABEL = "SAMPLE"
else:
    if has_raw():
        DATA_DIR  = RAW_DIR
        DATA_LABEL = "FULL (raw)"
    else:
        DATA_DIR  = SAMPLE_DIR
        DATA_LABEL = "SAMPLE"

# ── Load ──────────────────────────────────────────────────────────────────────
print("=" * 65)
print(f"META AD CAMPAIGN — DATA AUDIT  [{DATA_LABEL}]")
print("=" * 65)
print(f"\nLoading from: {DATA_DIR}")

suffix = "" if DATA_DIR == RAW_DIR else "_sample"

try:
    events    = pd.read_csv(os.path.join(DATA_DIR, f"ad_events{suffix}.csv"))
    ads       = pd.read_csv(os.path.join(DATA_DIR, f"ads{suffix}.csv"))
    campaigns = pd.read_csv(os.path.join(DATA_DIR, f"campaigns{suffix}.csv"))
    users     = pd.read_csv(os.path.join(DATA_DIR, f"users{suffix}.csv"))
except FileNotFoundError as e:
    sys.exit(f"\nFile not found: {e}\nRun from the repo root: python data/audit.py")

# ── 1. Row counts ─────────────────────────────────────────────────────────────
print("\n[1] ROW COUNTS")
print(f"  ad_events : {len(events):>10,}")
print(f"  ads       : {len(ads):>10,}")
print(f"  campaigns : {len(campaigns):>10,}")
print(f"  users     : {len(users):>10,}")
print()
print("  Full source reference: 400,000 / 200 / 50 / 9,841")

# ── 2. Primary key uniqueness ─────────────────────────────────────────────────
print("\n[2] PRIMARY KEY UNIQUENESS")

pk_checks = [
    ("ad_events[event_id]",    events,    "event_id"),
    ("ads[ad_id]",             ads,       "ad_id"),
    ("campaigns[campaign_id]", campaigns, "campaign_id"),
    ("users[user_id]",         users,     "user_id"),
]

all_ok = True
for label, df, col in pk_checks:
    n_rows   = len(df)
    n_unique = df[col].nunique()
    ok       = (n_rows == n_unique)
    if not ok:
        all_ok = False
    flag = "✅" if ok else f"❌  {n_rows - n_unique:,} duplicates"
    print(f"  {label:<35} {n_unique:>7,} / {n_rows:>7,}  {flag}")

if all_ok:
    print("  → All primary keys clean.")

# ── 3. Foreign key / join coverage ────────────────────────────────────────────
print("\n[3] JOIN COVERAGE")

def check_join(left, right, key, left_label, right_label):
    merged    = left[[key]].merge(right[[key]], on=key, how="left", indicator=True)
    matched   = (merged["_merge"] == "both").sum()
    total     = len(left)
    unmatched = total - matched
    pct       = matched / total * 100
    ok        = (unmatched == 0)
    flag      = "✅" if ok else f"⚠️   {unmatched:,} unmatched rows"
    print(f"  {left_label} → {right_label} on [{key}]: {pct:.2f}%  {flag}")
    return unmatched

check_join(events, ads,    "ad_id",       "ad_events", "ads")
check_join(ads,    campaigns, "campaign_id", "ads",    "campaigns")
unmatched_users = check_join(events, users, "user_id", "ad_events", "users")

if unmatched_users > 0:
    # Check for scientific notation (Excel silently converts hex IDs containing 'e')
    sci_ids = users[users["user_id"].astype(str).str.match(r"^[\d.]+[Ee][+\-]?\d+$")]
    # Check for leading-zero-stripped IDs (Excel treats all-numeric IDs as integers)
    lead_ids = users[users["user_id"].astype(str).str.match(r"^\d{1,4}$")]
    total_corrupt = len(sci_ids) + len(lead_ids)
    print(f"\n  Root cause — TWO Excel CSV-opening artifacts in users.csv:")
    print(f"    Artifact A — Scientific notation conversion : {len(sci_ids):,} IDs")
    print(f"    Sample: {list(sci_ids['user_id'].head(3))}")
    print(f"    Artifact B — Leading-zero stripping         : {len(lead_ids):,} IDs")
    print(f"    Sample: {list(lead_ids['user_id'].head(3))}")
    print(f"    Total corrupted user IDs                   : {total_corrupt:,} ({len(sci_ids)} sci-notation + {len(lead_ids)} leading-zero-stripped)")
    print(f"  Impact: {unmatched_users:,} events excluded from demographic breakdowns.")
    print(f"  These events still count in impression/click/purchase totals.")

print()
print("  Full source reference:")
print("    ad_events → ads       : 100.00% ✅")
print("    ads → campaigns       : 100.00% ✅")
print("    ad_events → users     : 94.99%  ⚠️  20,046 unmatched")
print("      Root cause: 289 sci-notation + 117 leading-zero-stripped = 406 corrupted user IDs")

# ── 4. Campaign window validation ─────────────────────────────────────────────
print("\n[4] CAMPAIGN WINDOW VALIDATION")
print("    Are event timestamps inside their linked campaign's active dates?")

ev_c = (events
    .merge(ads[["ad_id", "campaign_id"]], on="ad_id", how="left")
    .merge(campaigns[["campaign_id", "start_date", "end_date"]], on="campaign_id", how="left"))

ev_c["timestamp"]  = pd.to_datetime(ev_c["timestamp"])
ev_c["start_date"] = pd.to_datetime(ev_c["start_date"], dayfirst=True)
ev_c["end_date"]   = pd.to_datetime(ev_c["end_date"],   dayfirst=True)

outside     = ((ev_c["timestamp"] < ev_c["start_date"]) |
               (ev_c["timestamp"] > ev_c["end_date"])).sum()
pct_outside = outside / len(ev_c) * 100

flag = "✅" if outside == 0 else f"⚠️  {outside:,} rows ({pct_outside:.1f}%)"
print(f"  Events outside campaign window: {flag}")
print()
print("  Full source: 225,406 events (56.4%) fall outside their campaign window.")
print("  Likely cause: events were collected over a broader window (May–Aug 2025)")
print("  than the campaign date fields cover. Campaign dates aren't reliable")
print("  event boundaries in this dataset.")

# ── 5. Budget fanout ──────────────────────────────────────────────────────────
print("\n[5] BUDGET FANOUT")
print("    What happens when total_budget is joined to lower grains?")

correct  = campaigns["total_budget"].sum()
at_ads   = ads.merge(campaigns[["campaign_id","total_budget"]], on="campaign_id")["total_budget"].sum()
ev_camp  = (events
    .merge(ads[["ad_id","campaign_id"]], on="ad_id")
    .merge(campaigns[["campaign_id","total_budget"]], on="campaign_id"))
at_events = ev_camp["total_budget"].sum()

print(f"  Campaign grain (correct): ${correct:>18,.2f}  ×1")
print(f"  Joined to ads grain:      ${at_ads:>18,.2f}  ×{at_ads/correct:.0f}")
print(f"  Joined to events grain:   ${at_events:>18,.2f}  ×{at_events/correct:,.0f}")
print()
print("  All budget measures in the report pull from campaigns table only.")
print("  Never joined down or summed at a lower grain.")

# ── 6. Event type distribution ────────────────────────────────────────────────
print("\n[6] EVENT TYPE DISTRIBUTION")

total = len(events)
et    = events["event_type"].value_counts()
for event_type, count in et.items():
    bar = "█" * int(count / total * 40)
    print(f"  {event_type:<12}: {count:>8,}  ({count/total:5.1%})  {bar}")

# ── 7. Platform split ─────────────────────────────────────────────────────────
print("\n[7] PLATFORM SPLIT")
ev_ads = events.merge(ads[["ad_id","ad_platform"]], on="ad_id", how="left")
plat_counts = ev_ads["ad_platform"].value_counts()
for plat, n in plat_counts.items():
    print(f"  {plat}: {n:>8,}  ({n/len(ev_ads):.1%})")

# ── 8. Per-platform KPI check (Comments/Shares verified per platform) ─────────
print("\n[8] KPI SPOT-CHECK — PER PLATFORM (verified against raw data)")

for platform in ["Facebook", "Instagram"]:
    pf = ev_ads[ev_ads["ad_platform"] == platform]
    p_imp = (pf["event_type"] == "Impression").sum()
    p_clk = (pf["event_type"] == "Click").sum()
    p_pur = (pf["event_type"] == "Purchase").sum()
    p_com = (pf["event_type"] == "Comment").sum()
    p_shr = (pf["event_type"] == "Share").sum()
    p_lik = (pf["event_type"] == "Like").sum()
    p_eng = p_clk + p_com + p_shr
    p_ctr = p_clk / p_imp if p_imp else 0
    p_er  = p_eng / p_imp if p_imp else 0
    p_cvr = p_pur / p_clk if p_clk else 0
    p_pr  = p_pur / p_imp if p_imp else 0
    print(f"\n  {platform.upper()}")
    print(f"  Impressions    : {p_imp:>10,}")
    print(f"  Clicks         : {p_clk:>10,}")
    print(f"  Comments       : {p_com:>10,}   (excluded from Engagements? No — included)")
    print(f"  Shares         : {p_shr:>10,}   (included in Engagements)")
    print(f"  Likes          : {p_lik:>10,}   (tracked; excluded from Engagements)")
    print(f"  Purchases      : {p_pur:>10,}")
    print(f"  Engagements    : {p_eng:>10,}   (Clicks + Comments + Shares)")
    print(f"  CTR            : {p_ctr:>10.2%}")
    print(f"  Engagement Rate: {p_er:>10.2%}")
    print(f"  Conversion Rate: {p_cvr:>10.2%}")
    print(f"  Purchase Rate  : {p_pr:>10.2%}")

print()
print("  Full source reference (Facebook)  : 215,972 imp / 25,389 clk / 2,632 com / 1,275 shr / 29,296 eng / 1,323 pur")
print("  CTR=11.76%  ER=13.56%  CVR=5.21%  PR=0.61%")
print("  Full source reference (Instagram) : 123,840 imp / 14,690 clk / 1,476 com /   682 shr / 16,848 eng /   708 pur")
print("  CTR=11.86%  ER=13.60%  CVR=4.82%  PR=0.57%")
print()
print("  NOTE: Earlier versions of this script and the README incorrectly stated")
print("  FB Comments=2,680 / IG Comments=1,428 / FB Shares=1,227 / IG Shares=730.")
print("  Correct values: FB Comments=2,632 / IG Comments=1,476 / FB Shares=1,275 / IG Shares=682.")
print("  Combined totals (4,108 comments / 1,957 shares) are unaffected.")

# ── Done ──────────────────────────────────────────────────────────────────────
print()
print("=" * 65)
print("Audit complete.")
print("=" * 65)
