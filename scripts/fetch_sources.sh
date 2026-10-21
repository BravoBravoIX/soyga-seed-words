#!/usr/bin/env bash
# Download the public sources this study is built from, into SOURCE_DIR, and check
# them against the SHA-256 sums of the copies used for the published results.
# None of these files is redistributed here; each stays under its own terms.
# Needs git, curl, unzip and pdftotext (poppler).
# Usage: scripts/fetch_sources.sh SOURCE_DIR
set -euo pipefail
SUMS="$(cd "$(dirname "$0")/.." && pwd)/sources/SHA256SUMS"
OUT="$1"
mkdir -p "$OUT"/louv "$OUT"/teker
get() { [ -s "$2" ] || curl -fsSL --retry 3 -o "$2" "$1"; }

# orey/book-of-soyga: copies of the Reeds 1998 preprint and the Kupin 2014 edition,
# and that repository's generated tables (an independent implementation of Reeds's rule).
# Pinned to the commit the published results were made from.
OREY_COMMIT=49c72a231e980690696cf64a4bf7e6f8482b66ab
if [ ! -d "$OUT/orey/.git" ]; then
  git clone -q https://github.com/orey/book-of-soyga.git "$OUT/orey"
fi
git -C "$OUT/orey" checkout -q "$OREY_COMMIT"

# Jason Louv (2026), reproduction package, Zenodo 10.5281/zenodo.20696278
get https://zenodo.org/api/records/20696278/files/soyga-reproduction.zip/content "$OUT/louv/soyga-reproduction.zip"
(cd "$OUT/louv" && unzip -q -o soyga-reproduction.zip)

# Onur Teker (2026), preprint, supplement and code (CC BY 4.0), Zenodo 10.5281/zenodo.23431833
# (read for comparison; the pipeline does not use them)
for f in Teker_2026_Soyga_preprint_v1.5_submitted_text.pdf Soyga_Supplement_v1.6.pdf Soyga_v1.6_code.zip; do
  get "https://zenodo.org/api/records/23431833/files/$f/content" "$OUT/teker/$f"
done

# Onur Teker (2026), v1.7 supplement and its code (CC BY 4.0), Zenodo 10.5281/zenodo.23524253
# (read for comparison and credit; the pipeline does not use them)
for f in Soyga_Supplement_v1.7.pdf Soyga_v1.7_code.zip; do
  get "https://zenodo.org/api/records/23524253/files/$f/content" "$OUT/teker/$f"
done

# Text layers of the two PDFs, which the code reads
pdftotext -layout "$OUT/orey/1998 John Dee and the Magic Tables in the Book of Soyga - Jim Reeds.pdf" "$OUT/reeds.txt"
pdftotext -layout "$OUT/orey/2014 The Book of Soyga - Jane Kupin.pdf" "$OUT/kupin.txt"

cd "$OUT"
if sha256sum --quiet -c "$SUMS"; then
  echo "all sources match the copies used for the published results"
else
  echo "WARNING: a source differs from the copy used for the published results." >&2
  echo "The rebuild may still run, but results can differ (see README, How to reproduce)." >&2
fi
