#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p \
  "$ROOT_DIR/data/raw/openreview" \
  "$ROOT_DIR/data/raw/figshare" \
  "$ROOT_DIR/data/raw/kaggle"

echo "Fetching OpenReview paper..."
curl -L "https://openreview.net/pdf?id=heBKnuV42O" \
  -o "$ROOT_DIR/data/raw/openreview/openreview_paper_heBKnuV42O.pdf"

echo "Fetching CSympData Figshare file..."
curl -L "https://figshare.com/ndownloader/files/57688621" \
  -o "$ROOT_DIR/data/raw/figshare/csympdata_file_57688621"

cat <<'EOF'

Kaggle dataset acquisition still requires a manual or authenticated workflow.
Suggested target folder:
  data/raw/kaggle/

Dataset URL:
  https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset

EOF
