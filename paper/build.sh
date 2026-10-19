#!/bin/sh
# Builds paper/soyga-seed-words.pdf from the Typst source (needs uv; fetches the typst package).
cd "$(dirname "$0")" && uv run --no-project --with typst==0.15.0 python -c "import typst; typst.compile('soyga-seed-words.typ', output='soyga-seed-words.pdf')"
