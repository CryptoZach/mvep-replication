#!/usr/bin/env python3
"""exhibit_01_mvep_scorecard: consolidated MVEP v4 scorecard matrix.

Synthesizes the per-product MVEP verdicts of record in A2 PAPER.md into one
10-category-plus-CSA by product matrix, marking unassessed cells. Every of-record
cell is sourced to its origin in PAPER.md (Table 4 at Section 5.4; the v4 summary
table at Section 4.8; Findings 5 and 6; the per-product worked examples in the
Supplementary Materials). USYC is an offshore-comparator scoring (tag NEW),
flagged distinctly. The USYC Category 4 Custody verdict is AMBIGUOUS: the only
documented fund-asset custody is segregated accounts at prime
broker Marex Capital Markets, Inc. (per the Hashnote product-structuring docs);
no published segregation or bankruptcy-remoteness analysis; weaker than the
bank-custodian basis behind the comparators' PASS cells; OUSG dual-layer
AMBIGUOUS is the analog. The USYC Category 5 Insolvency verdict is PARTIAL.
The entire Category 5 row is derived from Exhibit 2
(exhibit_02_cat5_jurisdiction_matrix; source tag JX): USDT FAIL and JPMD
PARTIAL; USDY PARTIAL (J4xD4 fail caps at PARTIAL;
J4xD5 partial via the UCC 9-322 backstop; issuer migrated to Ondo Global
Markets (BVI) Limited 2025-12-15); USYC PARTIAL on the
J6 Cayman-fund controlling layer (the tokenholder is a direct registered
shareholder, no nominee).
Scale annotations: all per-product scale
annotations are grounded in the rwa.xyz platform snapshot of 2026-06-14
(treasuries
league table for the fund products incl. per-product holder counts,
stablecoins league table for the stablecoins; all holder counts are now
all-network platform-wide wallet-address counts, the basis rwa.xyz reports
directly; an Ethereum-chain Blockscout pull remains an on-chain cross-check; the
dagger convention is retired).
Key USYC facts: USD 3.01B AUM; 47 holders (largest tokenized
Treasury product, thinnest holder base in the comparator set); 0% mgmt / 10%
performance fee; Hashnote rebranded Circle USYC. The thin holder base plus
exclusive USDC subscription/redemption drives the Category 10 (Collateral
Operability) FAIL: no liquidation path independent of
USDC exists, and a 47-holder base (wallet-address count per platform data, not
an approved-investor count) cannot provide secondary-market depth under stress
(the Category 10 pass condition requires liquidation via at least one path
under EACH stress scenario). Franklin family note: rwa.xyz lists BENJI
(the 1940 Act fund this exhibit scores, CIK 0001786958) at USD 0.84B alongside
the iBENJI institutional fund (BVI Reg D, USD 1.60B) and gBENJI
(Luxembourg UCITS, USD 55M); the BENJI scale line reflects the assessed fund
only.

USD1 is a 12th column for the GENIUS-era stablecoin
(World Liberty Financial brand; issuer and redeemer of record BitGo Bank &
Trust, N.A., the OCC-chartered uninsured national trust bank converted from
BitGo Trust Company, Inc. (SD) per OCC conditional approval 2025-12-12;
USD 4.36B market cap per the rwa.xyz 2026-06-14 snapshot row; 411,779
all-network holders (44,053 on Ethereum via the 2026-06-11 Blockscout
cross-check); majority of supply
off-Ethereum across nine chains per CoinGecko, eleven networks per the issuer
contract registry). USD1 (tag NEW2) is scored across
all eleven cells against the product's primary documents and on-chain state:
Cat 1 FAIL; Cat 2 AMBIGUOUS records-at-multiple-layers; Cat 3 PARTIAL; Cat 4
AMBIGUOUS; Cat 5 AMBIGUOUS per the Exhibit 2 federal-layer (J3F) trust-stack
derivation; Cat 6 FAIL; Cat 7
NOT_DISCLOSED after a documented search; Cat 8 FAIL on on-chain verified
no-timelock upgradeable proxy plus bare-EOA mint and freeze keys; Cat 9 PARTIAL;
Cat 10
AMBIGUOUS on the documented-but-unproven liquidation paths; CSA PARTIAL on the
fiat-termination pattern via the regulated trust bank. Per-cell basis in
CAPTION.md and the paper's Supplementary Materials USD1 block.

The UNASSESSED display label is rendered as "Unassessed" (distinct from the
semantically separate Not disclosed verdict: Not
disclosed is an ASSESSED verdict after a documented search; Unassessed means no
assessment was performed), and the footer explains the single N/A cell
(BENJI Category 8: traditional fund, no on-chain admin keys, per Table 4).

Axis orientation: the rendered matrix has products as the X-axis columns and the
ten categories plus the recursive Cash Settlement Asset analysis as the Y-axis
rows. This matches the CSV orientation (category rows by product columns), so the
figure and the source CSV share one orientation and existing row-number citations
into mvep_scorecard_data.csv remain valid.

Partial-evidence cells and the PYUSD re-derivation (tag NEW3):
the fourteen Exhibit 1 cells classified
as PARTIAL-EVIDENCE candidates are scored on the comparator-scoring path
(primary documents plus on-chain reads): USDC Cat 2 AMBIGUOUS and Cat
9 PARTIAL; USDT Cat 4 FAIL and Cat 9 PARTIAL; USDG Cat 2 AMBIGUOUS and Cat 7
NOT_DISCLOSED; PYUSD Cat 2 AMBIGUOUS, Cat 7 NOT_DISCLOSED, Cat 8 FAIL; DAI Cat 4
FAIL and Cat 8 FAIL; JPMD Cat 4 AMBIGUOUS, Cat 8 FAIL, Cat 10 AMBIGUOUS. The
PYUSD Category 4 and Category 5 staleness review re-derives on the
consummated Paxos OCC conversion
(Charter 25379 on the OCC active trust-bank list as of 5/31/2026;
live Paxos terms name Paxos Trust Company, N.A. under OCC approval with zero NYDFS
references), so the federal-layer entity-scoping fires, the NYDFS custody layer
behind the Finding 5 PASS no longer reaches the issuer, and PYUSD Category 4
re-derives PASS to PARTIAL (NEW3; the terms carry affirmative segregation
covenants, an in-terms
bankruptcy-remoteness clause, and no property-interest disclaimer, so the explicit
leg passes where USD1's self-contradicting terms reached only AMBIGUOUS) while
Category 5 re-derives PARTIAL to AMBIGUOUS on the Exhibit 2 J3F row (the J3FxD5
fail-grade absence fires the Q1a cap, the affirmative contractual cure resolves it
to AMBIGUOUS rather than FAIL). USDC stays on J3 (Circle remains NYDFS-supervised);
USD1 unchanged.

SoFiUSD (tag NEW4) is a
thirteenth column for the first stablecoin issued by an FDIC-insured full-service
US national bank (SoFi Bank, N.A., FDIC Cert 26881, OCC-regulated; holding company
SoFi Technologies; two launches, enterprise 2025-12-18 and consumer-app
2026-05-27; ticker SOFID; Ethereum and Solana; approximately USD 0.15B per rwa.xyz
2026-06-12, thin parked supply). All eleven cells are graded:
Cat 1 FAIL, Cat 2 AMBIGUOUS, Cat 3 NOT_DISCLOSED, Cat 4 AMBIGUOUS, Cat 5 AMBIGUOUS
(Exhibit 2 J2S insured-bank non-deposit sub-row), Cat 6 FAIL, Cat 7 NOT_DISCLOSED,
Cat 8 FAIL, Cat 9 PARTIAL, Cat 10 AMBIGUOUS, Cash Settlement Asset PARTIAL. The
defining fact: SoFi Bank is FDIC-insured (unlike the uninsured OCC trust banks
behind USD1 and the converted Paxos entity), but SoFiUSD is expressly not a
deposit, so the holder's claim class in an FDIC receivership is the open question
the J2S sub-row scores. Per-cell basis in CAPTION.md and the Supplementary
Materials SoFiUSD block.

NO cell verdict is invented: cells with no of-record verdict and not newly scored
are marked UNASSESSED. Run: python3 exhibit_01_mvep_scorecard.py
Outputs (same dir): exhibit_01_mvep_scorecard.png and mvep_scorecard_data.csv.

Author: Tokenization Systems. Reproduction artifact; no external data dependency.
"""

import csv
from pathlib import Path

import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = Path(__file__).resolve().parent

# Verdict levels and their display + color.
# Legend uses full names; cells keep abbreviations for width.
LEGEND_LABELS = {"AMBIGUOUS": "Ambiguous", "NOT_DISCLOSED": "Not disclosed"}

LEVELS = {
    "PASS": ("Pass", "#2e7d32", "white"),
    "PARTIAL": ("Partial", "#9e9d24", "white"),
    "AMBIGUOUS": ("Ambig.", "#ef6c00", "white"),
    "FAIL": ("Fail", "#c62828", "white"),
    "NOT_DISCLOSED": ("Not disc.", "#90a4ae", "black"),
    "NA": ("N/A", "#455a64", "white"),
    "UNASSESSED": ("Unassessed", "#f5f5f5", "#9e9e9e"),
}

# Categories (rows). The ten MVEP categories plus the v4 recursive Cash
# Settlement Asset analysis as a distinct axis (the summary table breaks it out).
CATEGORIES = [
    "1. Rights Parity",
    "2. System of Record",
    "3. Records & Reconciliation",
    "4. Custody & Customer Property",
    "5. Insolvency Posture",
    "6. Settlement Finality",
    "7. Reorg & Exception Handling",
    "8. Governance & Change Control",
    "9. Disclosures",
    "10. Collateral Operability",
    "Cash Settlement Asset (v4 recursive)",
]

# Products (columns). Grouped: regulated stablecoins, unregulated/decentralized,
# tokenized funds, deposit token, then the three comparators (USDY in Table 4 but
# outside the nine-product sample; USYC the offshore Reg S comparator; USD1 the
# GENIUS-era comparator, audit-hardened 2026-06-12).
PRODUCTS = [
    "USDC\n(Circle)", "USDT\n(Tether)", "USDG\n(Paxos)", "PYUSD\n(PayPal)",
    "DAI\n(MakerDAO)", "BUIDL\n(BlackRock)", "OUSG\n(Ondo)", "BENJI\n(Franklin)",
    "JPMD\n(JPMorgan)", "USDY\n(Ondo)", "USYC\n(Circle/Hashnote)*",
    "USD1\n(WLF/BitGo)**", "SoFiUSD\n(SoFi Bank)***", "RLUSD\n(Ripple)",
]

# Scale annotations, single-source: rwa.xyz snapshot 2026-06-14 (all-network per-product
# market cap or AUM + all-network holder-address counts, the basis rwa.xyz now reports
# directly; supersedes the 2026-06-11 Ethereum-chain Blockscout pulls, which remain
# available as an on-chain cross-check). JPMD is a permissioned bank deposit token not
# tracked by rwa.xyz.
SCALE = [
    "$72.9B|43.5M h", "$186.6B|206M h", "$1.55B|26.7K h", "$2.7B|153.8K h",
    "$4.2B|3.9M h", "$2.4B | 108 h", "$0.56B | 58 h", "$0.82B | 1,111 h",
    "permissioned;\nno public data", "$2.2B | 18,882 h", "$3.0B | 47 h",
    "$4.4B|411.8K h", "$0.15B | 13 h", "$1.73B | n/a h",
]

# Verdict matrix. Key = product short code; value = dict category-index -> (verdict, source-tag).
# Source tags: T2 = Section 5.4 Table 4; SUM = Section 4.8 v4 summary table; F5/F6 = Findings 5/6;
# WE = worked example; NEW = USYC offshore comparator scoring;
# NEW2 = USD1 GENIUS-era comparator scoring (all eleven cells against primary
#       documents and on-chain state, see CAPTION.md);
# RWA = grounded in the rwa.xyz platform snapshot (scale source of record);
# CP = coverage-completion scoring (the nineteen previously-unassessed
#      operational, disclosure, collateral-operability, and recursive-settlement
#      cells), graded on the framework method (on-chain verification for governance;
#      documented search for reorg and disclosure artifacts) plus the products'
#      documented structure, with one external verification (USDY redemption);
#      per-cell basis in CAPTION.md coverage-completion table;
# JX = derived from the Exhibit 2 Category 5 jurisdiction matrix (exhibit_02_cat5_jurisdiction_matrix)
#      under its scoring rules (USD1 and PYUSD per the federal-layer J3F derivation).
# NEW5 = NYDFS-trust-charter comparator scoring (RLUSD column only): all eleven cells graded against the
#       product's primary documents (User Terms; signed Deloitte and Touche attestation; the NYDFS
#       trust-charter grant and the 2025 custodial-structures guidance) and the verified on-chain
#       implementation contract; headline Non-Equivalent, binding Category 1 Rights Parity FAIL. See CAPTION.
U = ("UNASSESSED", "")
M = {
    "USDC": {0:("FAIL","SUM/WE"),1:("AMBIGUOUS","NEW3"),2:("PARTIAL","F5"),3:("PASS","F5"),4:("PARTIAL","F5/JX"),5:("FAIL","SUM/WE"),6:("NOT_DISCLOSED","CP"),7:("FAIL","CP"),8:("PARTIAL","NEW3"),9:("PARTIAL","CP"),10:("FAIL","SUM/WE")},
    "USDT": {0:("FAIL","SUM/WE"),1:("AMBIGUOUS","CP"),2:("PARTIAL","CP"),3:("FAIL","NEW3"),4:("FAIL","JX"),5:("FAIL","SUM/WE"),6:("NOT_DISCLOSED","CP"),7:("FAIL","CP"),8:("PARTIAL","NEW3"),9:("PARTIAL","CP"),10:("FAIL","SUM/WE")},
    "USDG": {0:("FAIL","SUM"),1:("AMBIGUOUS","NEW3"),2:("PARTIAL","F5"),3:("PASS","F5"),4:("PARTIAL","F5/JX"),5:("FAIL","SUM"),6:("NOT_DISCLOSED","NEW3"),7:("FAIL","CP"),8:("PARTIAL","CP"),9:("PARTIAL","CP"),10:("PARTIAL","SUM")},
    "PYUSD":{0:("FAIL","SUM"),1:("AMBIGUOUS","NEW3"),2:("PARTIAL","F5"),3:("PARTIAL","NEW3"),4:("AMBIGUOUS","NEW3/JX"),5:("FAIL","SUM"),6:("NOT_DISCLOSED","NEW3"),7:("FAIL","NEW3"),8:("PARTIAL","CP"),9:("PARTIAL","CP"),10:("PARTIAL","SUM")},
    "DAI":  {0:("FAIL","SUM"),1:("PASS","F6"),2:("PASS","F6"),3:("FAIL","NEW3"),4:("FAIL","F6/JX"),5:("PARTIAL","SUM"),6:("PASS","F6"),7:("FAIL","NEW3"),8:("PASS","F6"),9:("AMBIGUOUS","CP"),10:("FAIL","SUM")},
    "BUIDL":{0:("FAIL","T2"),1:("PASS","T2"),2:("PARTIAL","T2"),3:("PASS","T2"),4:("AMBIGUOUS","T2/JX"),5:("PARTIAL","T2"),6:("NOT_DISCLOSED","T2"),7:("FAIL","T2"),8:("PARTIAL","T2"),9:("PASS","T2"),10:("FAIL","SUM/WE")},
    "OUSG": {0:("FAIL","T2"),1:("AMBIGUOUS","T2"),2:("PARTIAL","T2"),3:("AMBIGUOUS","T2"),4:("AMBIGUOUS","T2/JX"),5:("PARTIAL","T2"),6:("NOT_DISCLOSED","T2"),7:("FAIL","T2"),8:("PARTIAL","T2"),9:("AMBIGUOUS","T2"),10:("FAIL","SUM/WE")},
    "BENJI":{0:("FAIL","T2"),1:("PASS","T2"),2:("PASS","T2"),3:("PASS","T2"),4:("PASS","T2/JX"),5:("PARTIAL","T2"),6:("NOT_DISCLOSED","T2"),7:("FAIL","T2"),8:("PASS","T2"),9:("FAIL","T2"),10:("PARTIAL","SUM")},
    "JPMD": {0:("PARTIAL","SUM/WE"),1:("PASS","CP"),2:("PARTIAL","CP"),3:("AMBIGUOUS","NEW3"),4:("PARTIAL","JX"),5:("PARTIAL","SUM/WE"),6:("NOT_DISCLOSED","CP"),7:("FAIL","NEW3"),8:("NOT_DISCLOSED","CP"),9:("AMBIGUOUS","NEW3"),10:("PARTIAL","SUM/WE")},
    "USDY": {0:("FAIL","T2"),1:("PASS","T2"),2:("PARTIAL","T2"),3:("PASS","T2"),4:("PARTIAL","T2/JX"),5:("PARTIAL","T2"),6:("NOT_DISCLOSED","T2"),7:("FAIL","T2"),8:("PARTIAL","T2"),9:("PARTIAL","T2"),10:("FAIL","CP")},
    "USYC": {0:("FAIL","NEW"),1:("AMBIGUOUS","NEW"),2:("PARTIAL","NEW"),3:("AMBIGUOUS","NEW"),4:("PARTIAL","JX"),5:("PARTIAL","NEW"),6:("NOT_DISCLOSED","NEW"),7:("FAIL","NEW"),8:("PARTIAL","NEW/RWA"),9:("FAIL","NEW/RWA"),10:("FAIL","NEW")},
    "USD1": {0:("FAIL","NEW2"),1:("AMBIGUOUS","NEW2"),2:("PARTIAL","NEW2"),3:("AMBIGUOUS","NEW2"),4:("AMBIGUOUS","NEW2/JX"),5:("FAIL","NEW2"),6:("NOT_DISCLOSED","NEW2"),7:("FAIL","NEW2"),8:("PARTIAL","NEW2"),9:("AMBIGUOUS","NEW2"),10:("FAIL","NEW2")},
    "SoFiUSD":{0:("FAIL","NEW4"),1:("AMBIGUOUS","NEW4"),2:("NOT_DISCLOSED","NEW4"),3:("AMBIGUOUS","NEW4"),4:("AMBIGUOUS","NEW4/JX"),5:("FAIL","NEW4"),6:("NOT_DISCLOSED","NEW4"),7:("FAIL","NEW4"),8:("PARTIAL","NEW4"),9:("AMBIGUOUS","NEW4"),10:("PARTIAL","NEW4")},
    "RLUSD":{0:("FAIL","NEW5"),1:("PARTIAL","NEW5"),2:("PARTIAL","NEW5"),3:("PARTIAL","NEW5"),4:("PARTIAL","NEW5"),5:("PARTIAL","NEW5"),6:("PARTIAL","NEW5"),7:("FAIL","NEW5"),8:("PARTIAL","NEW5"),9:("PARTIAL","NEW5"),10:("PASS","NEW5")},
}
CODES = ["USDC","USDT","USDG","PYUSD","DAI","BUIDL","OUSG","BENJI","JPMD","USDY","USYC","USD1","SoFiUSD","RLUSD"]


def cell(code, row):
    return M[code].get(row, U)


def write_csv():
    out = HERE / "mvep_scorecard_data.csv"
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["category"] + CODES)
        w.writerow(["__source__"] + ["see cell suffix" for _ in CODES])
        for r, cat in enumerate(CATEGORIES):
            row = [cat]
            for code in CODES:
                v, src = cell(code, r)
                row.append(v if not src else f"{v} [{src}]")
            w.writerow(row)
    return out


def render():
    # Orientation: products = X-axis columns,
    # categories = Y-axis rows. The CSV keeps the category-row by product-column
    # orientation, which matches this rendering.
    nrows, ncols = len(CATEGORIES), len(PRODUCTS)
    fig, ax = plt.subplots(figsize=(0.95 * ncols + 4.6, 0.66 * nrows + 4.2))
    for r in range(nrows):
        for c, code in enumerate(CODES):
            v, src = cell(code, r)
            disp, bg, fg = LEVELS[v]
            ax.add_patch(plt.Rectangle((c, nrows - 1 - r), 1, 1, facecolor=bg,
                                       edgecolor="white", linewidth=1.4))
            label = disp
            cell_fs = 7.0 if v == "UNASSESSED" else 8.2
            ax.text(c + 0.5, nrows - 1 - r + 0.58, label, ha="center", va="center",
                    fontsize=cell_fs, color=fg, fontweight="bold")
            if src:
                ax.text(c + 0.5, nrows - 1 - r + 0.24, src, ha="center", va="center",
                        fontsize=5.8, color=fg, alpha=0.85)
    ax.set_xlim(0, ncols)
    ax.set_ylim(0, nrows)
    ax.set_xticks([c + 0.5 for c in range(ncols)])
    ax.set_xticklabels([f"{p}\n{sc}" for p, sc in zip(PRODUCTS, SCALE)], fontsize=8.0)
    ax.xaxis.tick_top()
    ax.set_yticks([nrows - 1 - r + 0.5 for r in range(nrows)])
    ax.set_yticklabels(CATEGORIES, fontsize=9.5)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    # Legend shows only the verdict levels that actually appear in the matrix, in a
    # fixed preferred order, so a level absent from the data (Unassessed, once every
    # cell is graded) does not clutter the key.
    present_levels = {cell(code, r)[0] for r in range(nrows) for code in CODES}
    legend_order = [k for k in ["PASS", "PARTIAL", "AMBIGUOUS", "FAIL", "NOT_DISCLOSED", "NA", "UNASSESSED"]
                    if k in present_levels]
    legend = [Patch(facecolor=LEVELS[k][1], edgecolor="white", label=LEGEND_LABELS.get(k, LEVELS[k][0]))
              for k in legend_order]
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.055),
              ncol=len(legend_order), fontsize=9.5, frameon=False, handlelength=1.1)
    ax.set_title(textwrap.fill("MVEP v4 scorecard: per-product verdicts across the ten categories and the recursive Cash Settlement Asset analysis", 60),
                 fontsize=24.0, fontweight="bold", pad=30)
    fig.tight_layout(rect=[0, 0.18, 1, 1])
    _p = ax.get_position()
    _fx = (_p.x0 + _p.x1) / 2.0
    fig.text(_fx, 0.045, textwrap.fill(
             "Cell suffix = verdict source (T2 = Section 5.4 Table 4; SUM = Section 4.8 v4 summary table; F5/F6 = Findings 5/6; WE = worked example; NEW = offshore-comparator scoring (USYC column only; per-category basis in the Supplementary Materials); NEW2 = GENIUS-era comparator scoring (USD1 column only; per-category basis in the Supplementary Materials); NEW3 = the fourteen partial-evidence cells across USDC, USDT, USDG, PYUSD, DAI, and JPMD, scored against primary documents and on-chain state, plus the PYUSD Category 4 and Category 5 re-derivation onto the J3F federal-layer stack (per-cell basis in the Supplementary Materials); NEW4 = SoFiUSD insured-national-bank comparator scoring 2026-06-12 (SoFiUSD column only; per-cell basis in the Supplementary Materials); NEW5 = NYDFS-trust-charter comparator scoring (RLUSD column only; graded against primary documents and the verified on-chain contract; per-cell basis in the Supplementary Materials); JX = Exhibit 2 Category 5 jurisdiction matrix cells;"
             "RWA = grounded in the rwa.xyz platform snapshot of 2026-06-14, which also supplies the scale line under each product column header: market cap or AUM, '| N h' = all-network holder-address count where tracked; JPMD shows no scale line because a permissioned bank deposit token has no public supply or holder register and is not listed on rwa.xyz). Holder counts are all-network platform-wide wallet-address counts (not approved-investor counts), the basis rwa.xyz now reports directly; the prior cycle's Ethereum-chain Blockscout pulls remain available as an on-chain cross-check. "
             "USYC* = offshore (Reg S) comparator scoring (rwa.xyz-grounded: \\$3.0B AUM, 47 holders, exclusive USDC subscription/redemption); no full worked-example narrative (product unavailable to U.S. persons). "
             "USD1** = GENIUS-era comparator scoring (rwa.xyz-grounded: \\$4.4B market cap; issued and redeemed by BitGo Bank & Trust, N.A., an OCC-chartered national trust bank; majority of supply off-Ethereum); no worked-example narrative. "
             "SoFiUSD*** = insured-national-bank comparator scoring (rwa.xyz-grounded: \\$0.15B across Ethereum and Solana, 2026-06-12; issued and redeemed by SoFi Bank, N.A., an FDIC-insured full-service national bank, yet expressly not a deposit; thin parked supply, thirteen all-network holders (three on Ethereum, ten on Solana)); the Category 5 cell derives from the Exhibit 2 J2S insured-bank non-deposit sub-row; no worked-example narrative. "
             "Unassessed = no of-record verdict exists (no assessment performed); distinct from Not disclosed, an ASSESSED verdict recording that a documented search found no published issuer artifact for the category. "
             "", width=215),
             ha="center", va="bottom", fontsize=7.5, color="#555555")
    png = HERE / "exhibit_01_mvep_scorecard.png"
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return png


if __name__ == "__main__":
    csv_path = write_csv()
    png_path = render()
    # Coverage summary for the operator.
    total = len(CATEGORIES) * len(CODES)
    assessed = sum(1 for code in CODES for r in range(len(CATEGORIES)) if cell(code, r) != U)
    newly = sum(1 for r in range(len(CATEGORIES)) if cell("USYC", r) != U)
    newly_usd1 = sum(1 for r in range(len(CATEGORIES)) if cell("USD1", r) != U)
    print(f"wrote {csv_path.name} and {png_path.name}")
    print(f"coverage: {assessed}/{total} cells have an of-record-or-new verdict; {total - assessed} unassessed")
    print(f"USYC newly scored cells: {newly}")
    print(f"USD1 newly scored cells: {newly_usd1}")
