# Exhibit 3: MVEP composite rating

**A non-compensatory composite rating that assigns each tokenized dollar product a per-dimension equivalence profile and a weakest-link headline, derived deterministically from the Exhibit 1 verdict matrix.**

The rating answers the operational question a risk committee asks after reading the scorecard: given eleven category verdicts, what is the product's rating? It is built as the next-level analog of the Exhibit 2 Category 5 aggregation rule (which collapses seven insolvency dimensions into one verdict non-compensatively); here the same discipline collapses the eleven category verdicts into a three-part equivalence profile and a single weakest-link headline. Products are on the X axis, consistent with Exhibit 1, grouped into the nine-product sample then the five comparators added to test the framework's reach (a dashed divider and a bracketed label mark each block), each block ordered left to right by overall strength so the sample structure and the within-block ranking both read directly. In the figure each cell's shade encodes the dimension strength on the 1.0 to 5.0 rung scale (5 = every cell Pass = full equivalence, which no product reaches) and its bold tag the gate verdict, with the binding constraint and the disclosure modifier surfaced as their own rows; this rendering replaced a gate-tier coloring that collapsed to a single color because the universal Legal ceiling forces Non-Equivalent across nearly every cell, leaving the strength notch and the binding constraint to do the visible discriminating.

## Why this is not a weighted scorecard

A weighted sum is compensatory: a strong category buys back a failure in another. That contradicts the paper's central finding (Finding 6) that the categories capture independent dimensions of equivalence risk rather than a single underlying factor, and the weakest-link logic the paper applies to composed products (equivalence is the minimum across layers). Under a weighted score, USDC would still rate investment-grade because it passes custody and records, telling a risk committee the opposite of what the paper proves: that the Rights Parity defect is dispositive for legal equivalence and cannot be offset. The framework also retired a numeric MVEP score (the v1 nine-category "X out of 9" scheme, superseded by the categorical verdict matrix); a single weighted number would reverse that evolution away from false precision. The rating is therefore non-compensatory by construction.

## The rule

**1. Three equivalence dimensions, not one scalar.** The paper tests three independently testable dimensions (Section 1.1; Section 4.2). Each category is assigned to the dimension(s) it bears on per PAPER.md Section 4.2:

- **Legal equivalence**: Categories 1 (Rights Parity), 5 (Insolvency Posture), and the customer-property leg of 4 (Custody).
- **Operational equivalence**: Categories 2 (System of Record), 3 (Records and Reconciliation), 7 (Reorg and Exception Handling), 8 (Governance and Change Control), the control-of-movements leg of 4, and the executability leg of 10 (Collateral Operability).
- **Economic equivalence**: Category 6 (Settlement Finality), the liquidation-at-value leg of 10, and the recursive Cash Settlement Asset analysis.

The cross-cutting categories (4 and 10) floor every dimension they bear on, which makes the rating stricter, as a diligence instrument should be. Category 9 (Disclosures) is reported as a separate **disclosure-adequacy** modifier, not a floor on the three equivalence dimensions, because it measures whether the operator disclosed the risks (a transparency overlay that, per Section 4.2, must reflect all three dimensions accurately) rather than a substantive equivalence layer; folding it into the floors would let a disclosure gap tank an otherwise-strong profile.

**2. A non-compensatory gate (the floor).** Each dimension grade is the worst verdict among its categories on the ordinal ladder

> Equivalent (Pass) > Substantially Equivalent (Partial) > Indeterminate (Ambiguous) > Opaque (Not disclosed) > Non-Equivalent (Fail)

A fatal failure in any gate category caps the dimension and can never be bought up. **Not disclosed caps the grade**: it sits below Indeterminate on the ladder, so a dimension with an undisclosed required category cannot rate above Opaque. This is distinct from Non-Equivalent (a known defect) and from coverage gaps. N/A (structurally inapplicable) is excluded from the floor; Unassessed is excluded and counted against coverage only.

**3. A subordinate strength notch (the within-tier ordering).** The gate alone is too lossy: nearly every product carries at least one Fail in each dimension (the universal Category 1 defect in Legal; governance or collateral operability elsewhere), so a pure floor collapses strong and weak products alike to Non-Equivalent. Each dimension therefore also carries a **strength** score, the mean ladder level (1.0 to 5.0) over its gradeable categories. Strength orders products within a tier without ever lifting the tier, the credit-rating letter-versus-notch pattern: a product that fails one category but is otherwise strong (BENJI, strength 3.5) is distinguished from one that is weak across the board (USDT, strength 2.1), though both share the Non-Equivalent gate. The headline carries an overall strength, the mean over all gradeable cells.

**4. A weakest-link headline.** The headline tier is the minimum gate across the three dimensions (never a weighted sum), annotated with the binding constraint (the dimension and category that drives it; ties broken toward the weaker-strength dimension, so the named constraint is the product's distinctive weakness).

**5. Coverage and confidence, reported separately from the grade.** Assessed gradeable cells over applicable (non-N/A) cells, the count of undisclosed (opacity) cells, and a HIGH / MEDIUM / LOW confidence band (assessed fraction at or above 0.8, 0.5 to 0.8, below 0.5). A thinly assessed product cannot masquerade as a clean one.

## The universal legal ceiling (a feature, not a defect)

Category 1 fails for every product in the sample except JPMD on the structural, market-wide UCC Article 12 qualifying-purchaser defect (Section 4.3), so the Legal dimension is gated at Non-Equivalent for all but JPMD and the weakest-link headline is Non-Equivalent for all but JPMD. The rating surfaces the paper's central finding (no product achieves equivalence) at a glance. Cross-product discrimination therefore lives in the strength notches, in the Operational and Economic tiers, in the within-Legal insolvency posture (Category 5) and custody (Category 4), and in the coverage band. The vector is the rating; the scalar headline is the thesis.

## Results (current verdict matrix of record, grouped: the nine-product sample then the five comparators, each ordered by overall strength)

| Product | Legal | Operational | Economic | Headline | Overall | Coverage | Confidence |
|---|---|---|---|---|---|---|---|
| **Nine-product sample** | | | | | | | |
| BENJI (Franklin) | Non-Equivalent 3.7 | Non-Equivalent 3.2 | Non-Equivalent 3.0 | Non-Equivalent | 3.5 | 11/11 | HIGH |
| JPMD (JPMorgan) | Indeterminate 3.7 | Non-Equivalent 3.0 | Indeterminate 3.7 | Non-Equivalent | 3.3 | 11/11 | HIGH |
| BUIDL (BlackRock) | Non-Equivalent 3.0 | Non-Equivalent 3.7 | Non-Equivalent 3.3 | Non-Equivalent | 3.2 | 11/11 | HIGH |
| USDG (Paxos) | Non-Equivalent 3.3 | Non-Equivalent 3.2 | Non-Equivalent 3.0 | Non-Equivalent | 3.0 | 11/11 | HIGH |
| DAI (MakerDAO) | Non-Equivalent 1.0 | Non-Equivalent 3.3 | Non-Equivalent 2.7 | Non-Equivalent | 2.9 | 11/11 | HIGH |
| PYUSD (PayPal) | Non-Equivalent 2.7 | Non-Equivalent 3.0 | Non-Equivalent 3.0 | Non-Equivalent | 2.8 | 11/11 | HIGH |
| USDC (Circle) | Non-Equivalent 3.3 | Non-Equivalent 3.2 | Non-Equivalent 2.0 | Non-Equivalent | 2.7 | 11/11 | HIGH |
| OUSG (Ondo) | Non-Equivalent 2.3 | Non-Equivalent 2.7 | Non-Equivalent 2.7 | Non-Equivalent | 2.6 | 11/11 | HIGH |
| USDT (Tether) | Non-Equivalent 1.0 | Non-Equivalent 2.5 | Non-Equivalent 2.0 | Non-Equivalent | 2.1 | 11/11 | HIGH |
| **Comparators** (added to test framework reach) | | | | | | | |
| USDY (Ondo) | Non-Equivalent 3.3 | Non-Equivalent 3.5 | Non-Equivalent 3.0 | Non-Equivalent | 3.2 | 11/11 | HIGH |
| RLUSD (Ripple) | Non-Equivalent 3.0 | Non-Equivalent 3.5 | Substantially Equivalent 4.3 | Non-Equivalent | 3.5 | 11/11 | HIGH |
| USD1 (WLF/BitGo) | Non-Equivalent 2.3 | Non-Equivalent 2.7 | Non-Equivalent 1.7 | Non-Equivalent | 2.4 | 11/11 | HIGH |
| USYC (Circle/Hashnote) | Non-Equivalent 2.7 | Non-Equivalent 2.3 | Non-Equivalent 2.0 | Non-Equivalent | 2.5 | 11/11 | HIGH |
| SoFiUSD (SoFi Bank) | Non-Equivalent 2.3 | Non-Equivalent 2.3 | Non-Equivalent 2.7 | Non-Equivalent | 2.5 | 11/11 | HIGH |

Reading: every product is gated Non-Equivalent at the headline (no product achieves equivalence; JPMD alone escapes the universal Legal Non-Equivalent gate, carrying the only Indeterminate Legal and Economic tiers). The strength notch and the three-dimension profile do the discriminating. Within the nine-product sample the tokenized funds lead (BENJI at overall strength 3.5, BUIDL close behind), the Tier 2 regulated stablecoins (USDG, USDC, PYUSD) sit in the middle, and USDT is at the floor; among the comparators the RLUSD NYDFS-trust-charter comparator leads (overall strength 3.5; RLUSD carries the strongest economic tier in the set on a fiat redemption path), with USDY next (overall strength 3.2) and USD1, USYC, and SoFiUSD below. JPMD is the strongest on legal equivalence specifically (the bank deposit token closest to passing) while a new on-chain governance Fail drags its operational tier. DAI inverts the pattern as the paper predicts (Finding 6): a strong operational tier (3.3) against a Non-Equivalent legal floor (1.0). JPMD is the only product whose Legal and Economic gates escape Non-Equivalent (Indeterminate, the bank deposit token closest to passing), held at a Non-Equivalent headline only by an on-chain Governance Fail; USDC's economic gate is its weak point (the Settlement Finality and Cash Settlement Asset Fails collapse it to strength 2.0).

## Validation (the acceptance test)

The rule is trustworthy only if it reproduces the paper's qualitative ordering from the matrix mechanically. The script asserts four checks on every run, all currently passing: (1) JPMD is the only product with a non-Non-Equivalent Legal gate (Finding 5: closest to passing); (2) USDT is the minimum overall strength (Tier 3, the paper's weakest); (3) every tokenized fund outranks every Tier 2 stablecoin by overall strength; (4) every Tier 2 stablecoin outranks USDT. If any check failed, the rule would be wrong, not the paper.

## Reproduction

`python3 exhibit_03_mvep_composite_rating.py` reads `../exhibit_01_mvep_scorecard/mvep_scorecard_data.csv` (the verdict matrix of record), applies the rule, and regenerates `exhibit_03_mvep_composite_rating.png` and `mvep_composite_rating_data.csv`, printing the rating table and the acceptance-test result. The rating is a pure deterministic function of Exhibit 1, so re-running after the verdict matrix updates regenerates the ratings; no external data dependency. No rating is invented: every grade traces to specific Exhibit 1 cells via the floor and the strength mean.

## Provenance

The rating is built on three design decisions: a vector profile plus a single weakest-link headline tier; Not disclosed caps the grade; an enhanced-matrix rendering in which strength is the primary visual channel (cell shade plus the number) and the gate verdict a bold tag, with the overall-strength rank, the binding constraint, and the disclosure modifier promoted from the CSV into their own rows, because a gate-tier coloring collapses to a near-uniform color (the universal Category 1 ceiling forces Non-Equivalent across nearly every cell). The rating data and the acceptance test are independent of the rendering. The rating is an analytical layer over Exhibit 1: the comparator columns (USYC, USD1, SoFiUSD) carry the bases recorded in their Exhibit 1 caveats, the SoFiUSD Category 5 letter carries the open AMBIGUOUS-versus-FAIL question recorded there, and the RLUSD column is a NYDFS-trust-charter comparator scoring (source tag NEW5) graded against the product's primary documents and the verified on-chain contract.
