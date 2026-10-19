#!/usr/bin/env bash
# Rerun the whole study. Usage: code/run_all.sh SOURCE_DIR   (filled by scripts/fetch_sources.sh)
# CPU only, Python 3 standard library only; under a minute on one CPU.
set -euo pipefail
SRC="$(cd "$1" && pwd)"
cd "$(dirname "$0")"
LOUV_TABLES="$(dirname "$(find "$SRC/louv" -name 'T01_*.txt' | head -1)")"
python3 extract_excerpts.py "$SRC/kupin.txt" "$SRC/reeds.txt"
nice -n 19 python3 reproduce.py "$LOUV_TABLES" "$SRC/orey/book-of-soyga-tables.txt"
python3 name_variants.py "$SRC/kupin.txt"
nice -n 19 python3 sec28.py
nice -n 19 python3 repair.py
nice -n 19 python3 witness_diffs.py
nice -n 19 python3 cancer_copies.py > /dev/null
nice -n 19 python3 rules.py > ../results/rules_stdout.txt
