#!/usr/bin/env python3
"""exhibit_03_mvep_composite_rating: a non-compensatory composite rating over Exhibit 1.

Assigns each tokenized dollar product a rating derived deterministically from the
per-category verdicts in Exhibit 1 (mvep_scorecard_data.csv). The rating is NOT a
weighted scorecard: a weighted sum is compensatory (a strong category buys back a
failure in another), which contradicts the paper's central finding that the
categories capture independent dimensions of equivalence risk rather than a single
underlying factor (PAPER.md Finding 6), and the weakest-link logic the paper uses
for composed products (equivalence is the minimum across layers). It is instead a
non-compensatory FLOOR aggregation, the next-level analog of the Exhibit 2 Category 5
Q1a aggregation rule (which collapses seven insolvency dimensions into one verdict
non-compensatively): here it collapses the eleven category verdicts into a
per-dimension grade and a weakest-link headline.

Design:
- VECTOR PROFILE, not a scalar. The paper tests three independently-testable
  equivalence dimensions (Section 1.1; Section 4.2): Legal (Categories 1, 5, plus the
  custody-as-customer-property leg of 4), Operational (Categories 2, 3, 7, 8, plus
  the control-of-movements leg of 4 and the executability leg of 10), Economic
  (Category 6, plus the liquidation-at-value leg of 10 and the recursive Cash
  Settlement Asset analysis). Each product gets a grade per dimension.
- FLOOR aggregation on the extended ordinal ladder
  PASS > PARTIAL > AMBIGUOUS > NOT_DISCLOSED > FAIL. A dimension grade is the worst
  ladder level among its categories that carry a gradeable verdict.
- NOT_DISCLOSED CAPS the grade: it sits below AMBIGUOUS
  on the ladder, so a dimension with an undisclosed required category cannot rate
  above Opaque. Distinct from FAIL (a known defect) and from UNASSESSED (not looked
  at). NA (structurally inapplicable, e.g. BENJI Category 8) is excluded from the
  floor. UNASSESSED is excluded from the floor and counted against coverage only.
- DISCLOSURE ADEQUACY (Category 9) is reported as a separate modifier, not a floor on
  the three equivalence dimensions: it measures whether the operator disclosed the
  risks (a transparency overlay that "must reflect all three dimensions accurately",
  Section 4.2), not a substantive equivalence layer. Folding it into the floors
  would let a disclosure gap tank the entire profile.
- HEADLINE TIER = weakest-link = the minimum of the three dimension grades, annotated
  with the binding constraint (the dimension and category that drives it). The single
  headline is the weakest-link, never a weighted sum.
- COVERAGE / CONFIDENCE is reported separately from the grade: assessed gradeable
  cells over applicable (non-NA) cells, the NOT_DISCLOSED (opacity) count, and a
  HIGH / MEDIUM / LOW confidence band. A thinly-assessed product cannot masquerade as
  a clean one.

Calibration note (the universal Category 1 ceiling). Category 1 (Rights Parity) fails
for every product in the sample except JPMD on the structural, market-wide UCC
Article 12 qualifying-purchaser defect (Section 4.3), so the Legal dimension is
ceilinged at Non-Equivalent for all but JPMD and the weakest-link headline is
Non-Equivalent for all but JPMD. This is a FEATURE, not a defect of the rating: it
surfaces the paper's central finding (no product achieves equivalence) at a glance.
Cross-product discrimination therefore lives in the Operational and Economic tiers,
in the within-Legal insolvency posture (Category 5) and custody (Category 4), and in
the coverage band. The vector is the rating; the scalar headline is the thesis.

Validation (the acceptance test the rule must pass): the rating must reproduce the
paper's qualitative ordering from the matrix mechanically. JPMD carries the only
non-Non-Equivalent Legal tier (Finding 5: closest to passing). The tokenized funds
(BENJI, BUIDL, OUSG) carry strong Economic tiers; USDY's Economic tier now reflects
its recursive Cash Settlement Asset fail (redemption into USDC). USDT and DAI fail across
dimensions. If the rule did not reproduce this, the rule would be wrong, not the
paper. The script prints the validation summary on each run.

Reads:  ../exhibit_01_mvep_scorecard/mvep_scorecard_data.csv (the verdict matrix of
        record; the rating is a pure function of it, so re-running after the matrix
        updates regenerates the ratings). No external data dependency.
Outputs (same dir): exhibit_03_mvep_composite_rating.png and
        mvep_composite_rating_data.csv.

Axis orientation and cell encoding. Products on the
X axis, consistent with Exhibit 1. The prior rendering
colored each cell by the GATE tier, which is near-invariant by construction (the
universal Category 1 ceiling forces Non-Equivalent across nearly every cell), so the
table collapsed to a wall of one color and lost the discrimination the rating
computes. The redesign makes STRENGTH the primary visual (cell shade and the large
number, on the 1.0 to 5.0 rung scale) and keeps the GATE as a bold colored tag (NON-EQ on nearly every
cell preserves the thesis without the monochrome wall). It adds three rows the prior
rendering left to the CSV: an overall-strength gauge with the cross-product rank, the
binding constraint (the dimension and category that drive the weakest link), and the
disclosure-adequacy modifier. Columns are GROUPED into the nine-product sample then the
five comparators added to test the framework's reach, each block ordered left to right by
overall strength (strongest first; the caption's Results table uses the same grouped order),
so a reader sees both the sample structure and the within-block ranking directly. Strength
shade and gate tag are independent channels: shade never implies a passing verdict.

Author: Tokenization Systems. Reproduction artifact.
"""

import csv
import re
from pathlib import Path

import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
SCORECARD_CSV = HERE.parent / "exhibit_01_mvep_scorecard" / "mvep_scorecard_data.csv"

# Extended ordinal ladder for non-compensatory floor aggregation.
# Higher is better. NOT_DISCLOSED caps below AMBIGUOUS;
# NA and UNASSESSED are not on the ladder (excluded from the floor).
LADDER = {"PASS": 5, "PARTIAL": 4, "AMBIGUOUS": 3, "NOT_DISCLOSED": 2, "FAIL": 1}
GRADEABLE = set(LADDER)  # verdicts that participate in the floor and count as assessed

# Rating tiers (the output vocabulary; deliberately distinct from the cell verdicts).
TIER_FROM_LEVEL = {
    5: "EQUIVALENT",
    4: "SUBSTANTIALLY_EQUIVALENT",
    3: "INDETERMINATE",
    2: "OPAQUE",
    1: "NON_EQUIVALENT",
    0: "UNRATED",
}
TIER_DISPLAY = {
    "EQUIVALENT": ("Equivalent", "#2e7d32", "white"),
    "SUBSTANTIALLY_EQUIVALENT": ("Substantially Eq.", "#9e9d24", "white"),
    "INDETERMINATE": ("Indeterminate", "#ef6c00", "white"),
    "OPAQUE": ("Opaque", "#607d8b", "white"),
    "NON_EQUIVALENT": ("Non-Equivalent", "#c62828", "white"),
    "UNRATED": ("Unrated", "#f5f5f5", "#9e9e9e"),
}

# Category-to-dimension membership (Section 4.2). A category may appear in more than
# one dimension; the cross-cutting categories (4 custody, 10 collateral operability)
# floor every dimension they bear on, which makes the rating stricter, as a diligence
# instrument should be. Category 9 (disclosures) is pulled out as a separate adequacy
# modifier rather than a floor. Keys are the 1-based category numbers; "CSA" is the
# recursive Cash Settlement Asset row.
DIMENSIONS = {
    "Legal": [1, 5, 4],
    "Operational": [2, 3, 7, 8, 4, 10],
    "Economic": [6, 10, "CSA"],
}
DISCLOSURE_CATEGORY = 9

# Product display order and labels (mirrors Exhibit 1 grouping).
PRODUCT_LABELS = {
    "USDC": "USDC\n(Circle)", "USDT": "USDT\n(Tether)", "USDG": "USDG\n(Paxos)",
    "PYUSD": "PYUSD\n(PayPal)", "DAI": "DAI\n(MakerDAO)", "BUIDL": "BUIDL\n(BlackRock)",
    "OUSG": "OUSG\n(Ondo)", "BENJI": "BENJI\n(Franklin)", "JPMD": "JPMD\n(JPMorgan)",
    "USDY": "USDY\n(Ondo)", "USYC": "USYC\n(Circle/Hashnote)", "USD1": "USD1\n(WLF/BitGo)",
    "SoFiUSD": "SoFiUSD\n(SoFi Bank)", "RLUSD": "RLUSD\n(Ripple)",
}

# The five comparators: a nine-product sample plus five comparators added to test the
# framework's reach (USDY in Table 4 but outside the nine-product sample; the offshore,
# GENIUS-era, insured-bank, and NYDFS-trust-charter comparators). The figure groups the
# nine-product sample first, then the comparators, each ordered by overall strength within
# its block, so the sample structure is visible at a glance instead of intermixed.
COMPARATORS = ("USDY", "USYC", "USD1", "SoFiUSD", "RLUSD")


def parse_scorecard():
    """Read Exhibit 1's CSV, strip source-tag suffixes, return {product: {row_key: verdict}}.

    row_key is the 1-based category number for Categories 1..10 and the string "CSA"
    for the recursive Cash Settlement Asset row.
    """
    with SCORECARD_CSV.open() as fh:
        rows = list(csv.reader(fh))
    header = rows[0]
    products = header[1:]
    data = {p: {} for p in products}
    for r in rows[1:]:
        label = r[0]
        if label == "__source__":
            continue
        m = re.match(r"\s*(\d+)\.", label)
        key = int(m.group(1)) if m else ("CSA" if "Cash Settlement" in label else label)
        for p, cell in zip(products, r[1:]):
            verdict = re.sub(r"\s*\[.*?\]\s*$", "", cell).strip()  # drop "[SUM/WE]" etc.
            data[p][key] = verdict
    return products, data


def dimension_grade(verdicts, cats):
    """Non-compensatory GATE plus a subordinate STRENGTH notch for a dimension.

    The GATE is the floor (worst verdict) over the dimension's gradeable categories:
    it sets the tier and a fatal failure can never be bought up. The STRENGTH is the
    mean ladder level over the same gradeable categories (1.0 to 5.0): it orders
    products WITHIN a tier without ever lifting the tier (the credit-rating
    letter-vs-notch pattern). This restores discrimination the bare floor loses (a
    product that fails one category but is otherwise strong is distinguished from one
    that fails throughout, though both share the gate tier).

    Returns (tier_name, strength, binding_key, binding_verdict, n_assessed). NA and
    UNASSESSED categories do not participate. If none is gradeable, dimension is
    UNRATED with strength 0.
    """
    floor_level = None
    binding = (None, None)
    levels = []
    for c in cats:
        v = verdicts.get(c, "UNASSESSED")
        if v not in GRADEABLE:
            continue
        lvl = LADDER[v]
        levels.append(lvl)
        if floor_level is None or lvl < floor_level:
            floor_level = lvl
            binding = (c, v)
    if floor_level is None:
        return "UNRATED", 0.0, None, None, 0
    strength = round(sum(levels) / len(levels), 1)
    return TIER_FROM_LEVEL[floor_level], strength, binding[0], binding[1], len(levels)


def coverage(verdicts):
    """Return (assessed, applicable, not_disclosed_count, confidence_band)."""
    applicable = 0
    assessed = 0
    nd = 0
    for key in list(range(1, 11)) + ["CSA"]:
        v = verdicts.get(key, "UNASSESSED")
        if v == "NA":
            continue  # structurally inapplicable: not part of the applicable base
        applicable += 1
        if v in GRADEABLE:
            assessed += 1
        if v == "NOT_DISCLOSED":
            nd += 1
    frac = assessed / applicable if applicable else 0.0
    band = "HIGH" if frac >= 0.8 else ("MEDIUM" if frac >= 0.5 else "LOW")
    return assessed, applicable, nd, band


def cat_name(key):
    names = {
        1: "Rights Parity", 2: "System of Record", 3: "Records & Reconciliation",
        4: "Custody", 5: "Insolvency Posture", 6: "Settlement Finality",
        7: "Reorg & Exception Handling", 8: "Governance & Change Control",
        9: "Disclosures", 10: "Collateral Operability", "CSA": "Cash Settlement Asset",
    }
    return names.get(key, str(key))


def rate(verdicts):
    """Compute the full rating record for one product."""
    dims = {}
    strengths = {}
    binds = {}
    for dname, cats in DIMENSIONS.items():
        tier, strength, bkey, bverdict, _n = dimension_grade(verdicts, cats)
        dims[dname] = tier
        strengths[dname] = strength
        binds[dname] = (bkey, bverdict)
    # Headline weakest-link over the three equivalence dimensions (rated ones only).
    # Tie-break the gate by the weaker strength so the binding dimension is the one a
    # diligence reader should look at first.
    rated = {d: (TIER_FROM_LEVEL_INV(t), strengths[d]) for d, t in dims.items() if t != "UNRATED"}
    if rated:
        worst_dim = min(rated, key=lambda d: rated[d])
        headline = dims[worst_dim]
        bkey, bverdict = binds[worst_dim]
        binding = f"{worst_dim} / {cat_name(bkey)} {bverdict}"
    else:
        headline, binding = "UNRATED", "no coverage"
    # Overall strength: mean ladder level over ALL gradeable cells (1..10 + CSA),
    # the within-tier ordering on top of the weakest-link gate. Never lifts the gate.
    all_levels = [LADDER[v] for k in list(range(1, 11)) + ["CSA"]
                  for v in [verdicts.get(k, "UNASSESSED")] if v in GRADEABLE]
    overall_strength = round(sum(all_levels) / len(all_levels), 1) if all_levels else 0.0
    # Disclosure adequacy modifier (Category 9).
    disc = verdicts.get(DISCLOSURE_CATEGORY, "UNASSESSED")
    disc_label = {
        "PASS": "Adequate", "PARTIAL": "Partial", "AMBIGUOUS": "Indeterminate",
        "NOT_DISCLOSED": "None published", "FAIL": "Inadequate",
        "UNASSESSED": "Unassessed", "NA": "N/A",
    }.get(disc, disc)
    assessed, applicable, nd, band = coverage(verdicts)
    return {
        "Legal": dims["Legal"], "Operational": dims["Operational"],
        "Economic": dims["Economic"], "Headline": headline, "Binding": binding,
        "LegalStrength": strengths["Legal"], "OperationalStrength": strengths["Operational"],
        "EconomicStrength": strengths["Economic"], "OverallStrength": overall_strength,
        "Disclosure": disc_label, "Coverage": f"{assessed}/{applicable}",
        "Confidence": band, "Opacity": nd,
    }


def TIER_FROM_LEVEL_INV(tier_name):
    """Map a tier name back to its ladder level (for the weakest-link min)."""
    inv = {v: k for k, v in TIER_FROM_LEVEL.items()}
    return inv[tier_name]


def write_csv(products, ratings):
    out = HERE / "mvep_composite_rating_data.csv"
    cols = ["Legal (gate)", "Legal strength", "Operational (gate)", "Operational strength",
            "Economic (gate)", "Economic strength", "Disclosure",
            "Headline (gate)", "Overall strength", "Binding constraint",
            "Coverage", "Confidence"]
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["product"] + cols)
        for p in products:
            r = ratings[p]
            w.writerow([p,
                        TIER_DISPLAY[r["Legal"]][0], r["LegalStrength"],
                        TIER_DISPLAY[r["Operational"]][0], r["OperationalStrength"],
                        TIER_DISPLAY[r["Economic"]][0], r["EconomicStrength"],
                        r["Disclosure"],
                        TIER_DISPLAY[r["Headline"]][0], r["OverallStrength"], r["Binding"],
                        r["Coverage"], r["Confidence"]])
    return out


# --- visual-encoding helpers for the rendering (2026-06-13 readability redesign) ---
# GATE tag = the non-compensatory verdict (the thesis channel); kept short for the cell.
GATE_TAG = {
    "EQUIVALENT": ("EQUIV", "#2e7d32"),
    "SUBSTANTIALLY_EQUIVALENT": ("SUB-EQ", "#9e9d24"),
    "INDETERMINATE": ("INDET", "#ef6c00"),
    "OPAQUE": ("OPAQUE", "#607d8b"),
    "NON_EQUIVALENT": ("NON-EQ", "#c62828"),
    "UNRATED": ("UNRATED", "#9e9e9e"),
}
# Dimension tints for the binding-constraint row (categorical, no pass/fail meaning).
DIM_TINT = {"Legal": "#8d6e63", "Operational": "#5c6bc0", "Economic": "#00897b"}
# STRENGTH ramp (the within-tier ordering channel): a light, single-hue cool ramp,
# deliberately NOT green/red, so a strong-but-still-failing cell never reads as passing.
_CMAP = plt.get_cmap("Blues")


def _strfill(s):
    """Map a strength score on the 1.0 to 5.0 rung scale to a pale-to-medium cool fill.

    The ramp spans the full 1 (all Fail) to 5 (all Pass = equivalence) scale; the ramp
    width is set so the achievable 1 to 4 band keeps strong contrast while the 5 anchor
    (true equivalence, which no product reaches) sits at the dark end.
    """
    t = max(0.0, min(1.0, (s - 1.0) / 4.0))
    return _CMAP(0.05 + 0.56 * t)


def _lum(rgba):
    """Relative luminance, for choosing dark vs light number text against the fill."""
    return 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]


def _binding_parts(b):
    """Split a binding string 'Dimension / Category VERDICT' into (dimension, category)."""
    if "/" not in b:
        return ("", b)
    dim, rest = [x.strip() for x in b.split("/", 1)]
    cat = re.sub(r"\s+(FAIL|Non-Equivalent|Indeterminate|Opaque|Substantially Eq\.?)\s*$",
                 "", rest).strip()
    return (dim, cat)


def render(products, ratings):
    # Products on the X axis, GROUPED: the nine-product sample first, then the five
    # comparators, each block ordered strongest to weakest by overall strength so the rank
    # reads left to right within the block and the sample-plus-comparators structure is
    # visible. Rows: an overall-strength gauge with the within-block rank; the three
    # equivalence dimensions (shade = strength, tag = gate verdict); the binding constraint;
    # and the disclosure modifier. Shade carries the discrimination the bare gate loses; the
    # tag carries the thesis (NON-EQ everywhere).
    by_strength = lambda x: -ratings[x]["OverallStrength"]
    sample = sorted([p for p in products if p not in COMPARATORS], key=by_strength)
    comps = sorted([p for p in products if p in COMPARATORS], key=by_strength)
    prods = sample + comps
    n = len(prods)
    n_sample = len(sample)
    rows = ["Overall\nstrength", "Legal\nequivalence", "Operational\nequivalence",
            "Economic\nequivalence", "Binds on\n(weakest link)", "Disclosure"]
    nr = len(rows)
    cw, ch = 1.0, 1.0
    gap = 0.13
    smax = 5.0  # the rung scale tops at 5 (all Pass = equivalence); no product reaches it
    fig, ax = plt.subplots(figsize=(0.94 * n + 3.4, 1.12 * nr + 5.4))

    def cell_xy(ci, ri):
        return ci * cw, (nr - 1 - ri) * ch

    for ci, p in enumerate(prods):
        r = ratings[p]
        # Overall-strength: a large readable number on white (rank above), with a thin
        # gauge bar set BELOW the number so the bar edge never cuts through the digits.
        rx, ry = cell_xy(ci, 0)
        ax.add_patch(Rectangle((rx, ry), cw, ch, facecolor="white",
                               edgecolor="white", linewidth=1.6))
        ov = r["OverallStrength"]
        frac = (ov - 1.0) / (smax - 1.0)
        rank_in_block = ci + 1 if ci < n_sample else ci - n_sample + 1
        ax.text(rx + cw / 2, ry + ch * 0.85, f"#{rank_in_block}", ha="center", va="center",
                fontsize=7.6, color="#90a4ae", fontweight="bold")
        ax.text(rx + cw / 2, ry + ch * 0.53, f"{ov}", ha="center", va="center",
                fontsize=16.5, fontweight="bold", color="#102027")
        bx0, bw = rx + gap, cw - 2 * gap
        ax.add_patch(Rectangle((bx0, ry + ch * 0.13), bw, ch * 0.11,
                               facecolor="#eceff1", edgecolor="none"))
        ax.add_patch(Rectangle((bx0, ry + ch * 0.13), bw * frac, ch * 0.11,
                               facecolor="#455a64", edgecolor="none"))
        # Three equivalence dimensions: shade = strength, bold tag = gate verdict.
        for ri, (col, skey) in enumerate([("Legal", "LegalStrength"),
                                          ("Operational", "OperationalStrength"),
                                          ("Economic", "EconomicStrength")], start=1):
            rx, ry = cell_xy(ci, ri)
            s = r[skey]
            tier = r[col]
            fc = _strfill(s)
            ax.add_patch(Rectangle((rx, ry), cw, ch, facecolor=fc,
                                   edgecolor="white", linewidth=1.6))
            numcol = "white" if _lum(fc) < 0.55 else "#102027"
            tag, tc = GATE_TAG[tier]
            ax.text(rx + cw / 2, ry + ch * 0.70, tag, ha="center", va="center",
                    fontsize=7.6, fontweight="bold", color=tc)
            ax.text(rx + cw / 2, ry + ch * 0.32, f"{s}", ha="center", va="center",
                    fontsize=13.5, fontweight="bold", color=numcol)
        # Binding constraint (the dimension and category that drive the weakest link).
        rx, ry = cell_xy(ci, 4)
        dim, cat = _binding_parts(r["Binding"])
        tint = DIM_TINT.get(dim, "#777777")
        ax.add_patch(Rectangle((rx, ry), cw, ch, facecolor=tint, alpha=0.15,
                               edgecolor="white", linewidth=1.6))
        ax.text(rx + cw / 2, ry + ch * 0.64, dim, ha="center", va="center",
                fontsize=7.4, fontweight="bold", color=tint)
        ax.text(rx + cw / 2, ry + ch * 0.29, textwrap.fill(cat, 13), ha="center",
                va="center", fontsize=6.7, color="#37474f", linespacing=0.9)
        # Disclosure modifier (+ coverage / confidence when not the HIGH 11/11 default).
        rx, ry = cell_xy(ci, 5)
        ax.add_patch(Rectangle((rx, ry), cw, ch, facecolor="#fafafa",
                               edgecolor="white", linewidth=1.6))
        disc = r["Disclosure"]
        dcol = {"Adequate": "#2e7d32", "Partial": "#f9a825",
                "None published": "#c62828"}.get(disc, "#607d8b")
        ax.text(rx + cw / 2, ry + ch * 0.60, textwrap.fill(disc, 10), ha="center",
                va="center", fontsize=6.9, fontweight="bold", color=dcol, linespacing=0.9)
        cov = r["Coverage"] + ("" if r["Confidence"] == "HIGH" else " " + r["Confidence"])
        ax.text(rx + cw / 2, ry + ch * 0.24, cov, ha="center", va="center",
                fontsize=6.3, color="#b0bec5")

    # Light separators framing the three equivalence-dimension rows.
    ax.plot([0, n * cw], [nr - 1, nr - 1], color="#cfd8dc", lw=1.0, zorder=5)
    ax.plot([0, n * cw], [nr - 4, nr - 4], color="#cfd8dc", lw=1.0, zorder=5)

    # Group structure: the nine-product sample (left block) vs the five comparators added
    # to test the framework's reach (right block). A dashed divider at the block boundary
    # plus a bracketed label under each block make the sample structure read at a glance,
    # without losing the within-block strength ranking.
    ax.plot([n_sample * cw, n_sample * cw], [0, nr * ch], color="#90a4ae", lw=1.4,
            zorder=6, linestyle=(0, (4, 2)))
    gb_y = -0.18
    for c0, c1, glabel in [(0, n_sample, "Nine-product sample"),
                           (n_sample, n, "Comparators (added to test framework reach)")]:
        ax.plot([c0 * cw + 0.10, c1 * cw - 0.10], [gb_y, gb_y], color="#607d8b", lw=1.4, zorder=6)
        ax.plot([c0 * cw + 0.10, c0 * cw + 0.10], [gb_y, gb_y + 0.09], color="#607d8b", lw=1.4, zorder=6)
        ax.plot([c1 * cw - 0.10, c1 * cw - 0.10], [gb_y, gb_y + 0.09], color="#607d8b", lw=1.4, zorder=6)
        ax.text((c0 + c1) / 2 * cw, gb_y - 0.14, glabel, ha="center", va="top",
                fontsize=8.0, fontweight="bold", color="#37474f")

    # Legend strip below the grid: strength gradient + the gate tags that appear. Shifted
    # down to clear the group-label band added above.
    ly0, ly1 = -1.65, -1.05
    sw_x0, sw_w, nseg = 0.2, 3.0, 24
    for k in range(nseg):
        t = k / (nseg - 1)
        ax.add_patch(Rectangle((sw_x0 + sw_w * k / nseg, ly0), sw_w / nseg, ly1 - ly0,
                               facecolor=_CMAP(0.05 + 0.56 * t), edgecolor="none"))
    # Mark the best observed strength so the dark band above it reads as headroom no
    # product reaches; 5 = all Pass = equivalence. Computed from the rated dimension cells
    # (the values the shade encodes), not hardcoded, so it tracks the sample as products
    # are added or rescored (e.g. RLUSD's Economic 4.3 raised it past USDY's prior 4.0).
    best_obs = max(r[k] for r in ratings.values()
                   for k in ("LegalStrength", "OperationalStrength", "EconomicStrength"))
    sw_obs = sw_x0 + sw_w * (best_obs - 1.0) / (5.0 - 1.0)
    ax.plot([sw_obs, sw_obs], [ly0, ly1], color="#ffffff", lw=1.1)
    ax.text(sw_obs, ly0 - 0.04, f"best obs. {best_obs}", ha="center", va="top", fontsize=5.6, color="#78909c")
    ax.text(sw_x0, ly1 + 0.12, "weaker (1)", ha="left", va="bottom", fontsize=7, color="#78909c")
    ax.text(sw_x0 + sw_w, ly1 + 0.12, "stronger (5 = equivalence)", ha="right", va="bottom", fontsize=7, color="#78909c")
    ax.text(sw_x0 + sw_w / 2, (ly0 + ly1) / 2, "shade = STRENGTH (mean score, 1 to 5)",
            ha="center", va="center", fontsize=7, color="#37474f", fontweight="bold")
    # Gate-tag legend on its own line, spelling the full verdict names so NON-EQ, INDET,
    # and SUB-EQ are unambiguous (INDET = Indeterminate, the partial-information verdict
    # where the evidence neither passes nor fails the category).
    gately = ly0 - 0.60
    # Pin the x data-limit before laying out the gate legend so the data-to-pixel
    # transform is final, then advance the cursor by each label's ACTUAL rendered
    # width (measured in pixels, converted back to data units) instead of magic
    # per-character data-unit coefficients. The coefficient form drifts whenever the
    # figure width changes (the wide gloss lines under bbox_inches="tight" set the
    # scale), so a measured advance is scale-independent and stays tight.
    ax.set_xlim(0, n * cw)
    fig.canvas.draw()
    _rend = fig.canvas.get_renderer()
    _inv = ax.transData.inverted()

    def _wadv(t, pad):
        bb = t.get_window_extent(renderer=_rend)
        (x0, _) = _inv.transform((bb.x0, bb.y0))
        (x1, _) = _inv.transform((bb.x1, bb.y1))
        return (x1 - x0) + pad

    gx = 0.2
    gate_txt = ax.text(gx, gately, "GATE:", ha="left", va="center", fontsize=7.4,
                       color="#37474f", fontweight="bold")
    gx += _wadv(gate_txt, 0.30)
    for tier, full in [("NON_EQUIVALENT", "Non-Equivalent"),
                       ("INDETERMINATE", "Indeterminate"),
                       ("SUBSTANTIALLY_EQUIVALENT", "Substantially Eq.")]:
        tag, tc = GATE_TAG[tier]
        tag_txt = ax.text(gx, gately, tag, ha="left", va="center", fontsize=7.6,
                          fontweight="bold", color=tc)
        gx += _wadv(tag_txt, 0.18)
        full_txt = ax.text(gx, gately, full, ha="left", va="center", fontsize=7.2, color="#607d8b")
        gx += _wadv(full_txt, 0.55)

    # Weakest-link key: a brief plain-language gloss of each binding category (sourced
    # from PAPER.md Sections 4.2 to 5.1), so the 'Binds on' row reads in full for every
    # product. The bullet color encodes the dimension, matching the 'Binds on' cells.
    ky = gately - 0.62
    ax.text(0.2, ky, "Weakest link, by binding category (the cell that drives each product's Non-Equivalent headline):",
            ha="left", va="center", fontsize=7.9, fontweight="bold", color="#37474f")
    gloss = [
        ("Legal", "Rights Parity",
         "the token's rights do not match the underlying claim; the UCC Article 12 take-free protection is broken market-wide and left unrepaired (the universal ceiling that gates every product)."),
        ("Economic", "Settlement Finality",
         "on-chain block-confirmation finality omits the value-integrity and convertibility conditions the product is marketed with (in the SVB depeg, transfers 'settled' on-chain while valued at $0.87)."),
        ("Economic", "Collateral Operability",
         "the token posts as collateral instantly, but converting it back to cash under stress depends on redemption paths that can all be constrained or unavailable at once."),
        ("Operational", "Governance & Change Control",
         "changes are not demonstrably logged, approved, and reversible against a documented admin-key and change-control policy (JPMD carries a new on-chain governance Fail)."),
    ]
    for j, (dim, cat, meaning) in enumerate(gloss):
        yy = ky - 0.40 * (j + 1)
        ax.add_patch(Rectangle((0.26, yy - 0.10), 0.18, 0.20, facecolor=DIM_TINT[dim], edgecolor="none"))
        ax.text(0.62, yy, f"{cat} ({dim}): {meaning}", ha="left", va="center",
                fontsize=7.2, color="#455a64")
    key_bottom = ky - 0.40 * (len(gloss) + 0.7)

    ax.set_xlim(0, n * cw)
    ax.set_ylim(key_bottom, nr * ch)
    ax.set_xticks([ci * cw + cw / 2 for ci in range(n)])
    ax.set_xticklabels([PRODUCT_LABELS.get(p, p) for p in prods], fontsize=8.2)
    ax.xaxis.tick_top()
    ax.set_yticks([(nr - 1 - ri) * ch + ch / 2 for ri in range(nr)])
    ax.set_yticklabels(rows, fontsize=9.0)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_title(textwrap.fill(
        "MVEP composite rating: non-compensatory equivalence profile per product "
        "(every product Non-Equivalent at the weakest-link gate; strength discriminates within)", 84),
        fontsize=13.5, fontweight="bold", pad=26)
    foot = ("STRENGTH (the shade and the number) scores each Exhibit 1 cell on the rung scale Pass = 5, Partial = 4, Ambiguous = 3, "
            "Not-disclosed = 2, Fail = 1. Each dimension's strength is the mean score over its categories; the OVERALL strength (top row) is the "
            "mean score over all eleven gradeable cells (the ten categories plus the recursive Cash Settlement Asset; Not-applicable and "
            "Unassessed cells are excluded). The scale runs to 5 (every cell Pass = full equivalence); no product reaches it (the achievable "
            "ceiling is about 4.6, since the market-wide Rights Parity defect pins one cell at 1). Strength sets the left-to-right ranking but "
            "never lifts the non-compensatory gate, which holds every product at Non-Equivalent except JPMD on the Legal tier. Deterministic "
            "function of Exhibit 1.")
    fig.text(0.5, 0.018, textwrap.fill(foot, 178), ha="center", fontsize=7.3, color="#546e7a")
    fig.tight_layout(rect=[0, 0.05, 1, 0.965])
    png = HERE / "exhibit_03_mvep_composite_rating.png"
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return png


if __name__ == "__main__":
    products, data = parse_scorecard()
    ratings = {p: rate(data[p]) for p in products}
    csv_path = write_csv(products, ratings)
    png_path = render(products, ratings)
    print(f"wrote {csv_path.name} and {png_path.name}")
    print(f"rated {len(products)} products from {SCORECARD_CSV.name}\n")
    short = {"EQUIVALENT": "Equiv", "SUBSTANTIALLY_EQUIVALENT": "Subst.Eq",
             "INDETERMINATE": "Indet", "OPAQUE": "Opaque",
             "NON_EQUIVALENT": "Non-Eq", "UNRATED": "Unrated"}
    hdr = f"{'product':9s} {'Legal':14s} {'Operational':14s} {'Economic':14s} {'Headline':12s} {'ovr':4s} {'cov':6s} {'conf':6s}"
    print(hdr)
    print("-" * len(hdr))
    # Print sorted by overall strength within the headline gate, to show the within-tier ordering.
    for p in sorted(products, key=lambda x: (-TIER_FROM_LEVEL_INV(ratings[x]['Headline']),
                                             -ratings[x]['OverallStrength'])):
        r = ratings[p]
        print(f"{p:9s} {short[r['Legal']]+' '+str(r['LegalStrength']):14s} "
              f"{short[r['Operational']]+' '+str(r['OperationalStrength']):14s} "
              f"{short[r['Economic']]+' '+str(r['EconomicStrength']):14s} "
              f"{short[r['Headline']]:12s} {r['OverallStrength']:<4} "
              f"{r['Coverage']:6s} {r['Confidence']:6s}  binds: {r['Binding']}")
    print("\n--- VALIDATION (acceptance test: must reproduce the paper's ordering) ---")
    ov = {p: ratings[p]["OverallStrength"] for p in products}
    checks = []
    # 1. JPMD carries the only non-Non-Equivalent Legal gate (Finding 5: closest to passing).
    legal_non_ne = [p for p in products if ratings[p]["Legal"] != "NON_EQUIVALENT"]
    checks.append(("JPMD is the only product with a non-Non-Equivalent Legal gate",
                   legal_non_ne == ["JPMD"]))
    # 2. USDT (Tier 3, the paper's weakest) is the minimum overall strength.
    checks.append(("USDT is the minimum overall strength",
                   min(ov, key=ov.get) == "USDT"))
    # 3. Tokenized funds outrank the Tier 2 stablecoins by overall strength (Finding 5 tiering).
    funds = [p for p in ["BENJI", "BUIDL", "USDY"] if p in ov]
    tier2 = [p for p in ["USDC", "USDG", "PYUSD"] if p in ov]
    checks.append(("every tokenized fund outranks every Tier 2 stablecoin by overall strength",
                   funds and tier2 and min(ov[f] for f in funds) > max(ov[t] for t in tier2)))
    # 4. Tier 2 stablecoins outrank USDT (Tier 3) by overall strength.
    checks.append(("every Tier 2 stablecoin outranks USDT by overall strength",
                   tier2 and min(ov[t] for t in tier2) > ov.get("USDT", 0)))
    for desc, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}")
    allok = all(ok for _, ok in checks)
    print(f"  => acceptance test {'PASSED' if allok else 'FAILED'}: rating "
          f"{'reproduces' if allok else 'does NOT reproduce'} the paper's qualitative ordering.")
