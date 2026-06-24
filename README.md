# A2 MVEP replication package

Self-contained code and data to regenerate the three exhibits of "Minimum Viable Equivalence Pack: An Institutional Diligence Framework for Tokenized Products" (manuscript of record on SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6363138).

MVEP is a buyer-side diligence gate: it returns a per-category verdict on whether a tokenized product is what it claims to be, run by the party at risk rather than by the issuer. That is what distinguishes it from an issuer-paid credit rating, and the same ten-category structure extends to AI operators as MVEP-AI.

## What this reproduces

This is a framework and legal-analysis paper, not an econometric one, so the exhibits are not regression outputs. They are deterministic renderings and aggregations of the paper's per-product, per-category MVEP verdict matrix (the analytical result of the category-by-category assessment developed in the Article and its Supplementary Materials). The scripts encode that verdict matrix and the aggregation rules transparently, so a reader can audit every cell, every source tag, and the exact rule by which the composite rating is derived.

The package reproduces:

1. Exhibit 1, the consolidated MVEP v4 scorecard: eleven assessment categories (the ten MVEP categories plus the recursive Cash Settlement Asset row) across fourteen products (the nine-product sample plus the USDY, USYC, USD1, SoFiUSD, and RLUSD comparators), 154 cells in all, each carrying a verdict and a source tag that points to where in the Article the verdict is established.
2. Exhibit 2, the Category 5 (Insolvency Posture) jurisdiction matrix: twelve product-sample regimes (J1 to J10 plus the J2S FDIC-insured-bank non-deposit-stablecoin and J3F OCC-trust-bank federal-layer sub-rows) and eight international comparators (J11 EU MiCA, J12 UK, J13 Hong Kong, J14 UAE federal, J14A Abu Dhabi ADGM free zone, J14Z Dubai VARA free zone, J15 Switzerland, J16 Japan), twenty regimes in all, scored on seven insolvency-posture dimensions (D1 to D7); 49 pass, 61 partial, 21 fail, 9 fail-by-structural-inapplicability across 140 cells, each carrying a verdict and a primary-source basis.
3. Exhibit 3, the MVEP composite rating: a non-compensatory equivalence profile that is a deterministic function of Exhibit 1. It applies a floor (worst verdict) aggregation per equivalence dimension on the ordinal ladder Equivalent > Substantially-Equivalent > Indeterminate > Opaque > Non-Equivalent, plus a subordinate strength score (the mean rung on the 1-to-5 ladder Fail 1 to Pass 5). It is not a weighted score: a strong category cannot offset a failure. On every run it prints an acceptance test that asserts the rating reproduces the paper's qualitative ordering (for example, that JPMD carries the only non-Non-Equivalent Legal gate, and that USDT is the minimum overall strength); if any check failed, the rule, not the paper, would be wrong.

Because Exhibit 3 is computed mechanically from Exhibit 1, the package demonstrates that the composite rating is reproducible from the verdict matrix rather than hand-assigned. Exhibit 1's verdict matrix and Exhibit 2's jurisdiction matrix are the encoded analytical judgments of the Article; their per-cell provenance lives in the source tags (Exhibit 1) and evidence-basis strings (Exhibit 2), and is documented in full in each exhibit's `CAPTION.md`.

## Contents

```
replication/
  README.md            this file
  requirements.txt     pinned stack (matplotlib; standard library otherwise)
  reproduce.sh         regenerate all three exhibits in dependency order
  LICENSE
  exhibits/
    exhibit_01_mvep_scorecard/
      exhibit_01_mvep_scorecard.py   encodes the verdict matrix; renders the scorecard
      mvep_scorecard_data.csv        the verdict matrix with per-cell source tags (committed reference output)
      exhibit_01_mvep_scorecard.png  committed reference figure
      CAPTION.md                     methodology, per-cell scoring bases, source-tag legend
    exhibit_02_cat5_jurisdiction_matrix/
      exhibit_02_cat5_jurisdiction_matrix.py
      cat5_jurisdiction_matrix_data.csv
      exhibit_02_cat5_jurisdiction_matrix.png
      CAPTION.md
    exhibit_03_mvep_composite_rating/
      exhibit_03_mvep_composite_rating.py   the floor + strength aggregation over Exhibit 1
      mvep_composite_rating_data.csv         the per-product rating record (committed reference output)
      exhibit_03_mvep_composite_rating.png   committed reference figure
      CAPTION.md
```

Each exhibit script resolves its own paths from `__file__` and writes its outputs next to itself. Exhibit 3 reads `../exhibit_01_mvep_scorecard/mvep_scorecard_data.csv`, so the directory layout above must be preserved and Exhibit 1 must be run before Exhibit 3 (`reproduce.sh` enforces the order).

## Reproduce

```
python3 -m pip install -r requirements.txt
./reproduce.sh
```

Expected runtime is a few seconds. The run regenerates the three PNGs and the three data CSVs under `exhibits/`. To confirm an exact reproduction, diff the regenerated CSVs against the committed copies:

```
git diff --stat exhibits/*/*.csv     # expect no changes
```

The data CSVs and every printed number are deterministic and reproduce exactly on any platform. The acceptance test in the Exhibit 3 run prints `acceptance test PASSED`.

| Output | Producer |
|---|---|
| `exhibits/exhibit_01_mvep_scorecard/mvep_scorecard_data.csv` + `.png` | exhibit_01_mvep_scorecard.py |
| `exhibits/exhibit_02_cat5_jurisdiction_matrix/cat5_jurisdiction_matrix_data.csv` + `.png` | exhibit_02_cat5_jurisdiction_matrix.py |
| `exhibits/exhibit_03_mvep_composite_rating/mvep_composite_rating_data.csv` + `.png` | exhibit_03_mvep_composite_rating.py |

## Provenance

This package corresponds to the manuscript state of the SSRN version of record (abstract 6363138). The exhibit scripts are snapshots of the generators used for the Article, so a future revision of the Article may advance them ahead of this package. The verdict matrix and the jurisdiction matrix encode the legal and structural assessments developed in the Article; the per-cell bases (Exhibit 1 source tags such as T2, SUM, NEW3; Exhibit 2 JnxDn evidence strings) are explained in each exhibit's `CAPTION.md` and in the Article's Supplementary Materials.

## License

See `LICENSE`.
