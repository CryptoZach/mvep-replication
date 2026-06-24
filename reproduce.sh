#!/usr/bin/env bash
#
# Regenerate all three A2 MVEP exhibits (data CSVs + PNGs) from the encoded verdict
# matrix and aggregation rules. Each script resolves its own paths from __file__, so
# this runs correctly from any working directory.
#
# Order matters: Exhibit 1 writes the per-product verdict matrix that Exhibit 3 reads.
#
# Usage:
#   python3 -m pip install -r requirements.txt
#   ./reproduce.sh
#
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
EX="$HERE/exhibits"

echo "[1/3] Exhibit 1  MVEP v4 scorecard"
echo "      encodes the 11-category x 14-product verdict matrix; writes mvep_scorecard_data.csv + PNG"
python3 "$EX/exhibit_01_mvep_scorecard/exhibit_01_mvep_scorecard.py"
echo

echo "[2/3] Exhibit 2  Category 5 jurisdiction matrix"
echo "      encodes the 19-jurisdiction x 7-dimension insolvency matrix; writes cat5_jurisdiction_matrix_data.csv + PNG"
python3 "$EX/exhibit_02_cat5_jurisdiction_matrix/exhibit_02_cat5_jurisdiction_matrix.py"
echo

echo "[3/3] Exhibit 3  MVEP composite rating"
echo "      a deterministic function of Exhibit 1: applies the non-compensatory floor + 1-to-5 strength rule,"
echo "      writes mvep_composite_rating_data.csv + PNG, and runs the acceptance test"
echo "      (asserts the rating reproduces the paper's qualitative ordering)"
python3 "$EX/exhibit_03_mvep_composite_rating/exhibit_03_mvep_composite_rating.py"
echo

echo "Done. Regenerated the three exhibit PNGs and data CSVs under exhibits/."
echo "Diff the regenerated CSVs against the committed copies to confirm an exact reproduction."
