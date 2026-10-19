"""Rebuild data/manuscript_excerpts.json from the fetched sources (not redistributed).

The only cell-level manuscript readings in print that we could find:
  T1 'Aries', Sloane 8 ff. 102v-103r, first six rows, as printed in Kupin 2014 p. 532
     ('?' = illegible; 'ÿ' read as y);
  T5 'Leo', first 13 rows, as transcribed in Reeds 1998 p. 8.

Usage: extract_excerpts.py KUPIN_TXT REEDS_TXT   (pdftotext -layout output)
Writes data/manuscript_excerpts.json (ignored by git).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def kupin_t1(txt):
    pages = open(txt, encoding="utf-8").read().split("\f")
    page = next(p for p in pages if "[102v-103r]" in p and "TABULA" in p and "ARIES" in p)
    lines = page.splitlines()
    i = next(k for k, ln in enumerate(lines) if "TABULA" in ln and "ARIES" in ln)
    rows = []
    for ln in lines[i + 1 :]:
        row = "".join(ln.split()).replace("ÿ", "y")
        if not row:
            continue
        if len(row) != 36:
            break
        rows.append(row)
    assert len(rows) == 6, rows
    return rows


def reeds_t5(txt):
    lines = open(txt, encoding="utf-8").read().splitlines()
    i = next(k for k, ln in enumerate(lines) if "T5" in ln and "Leo" in ln and "triangular" in ln)
    rows = []
    for ln in lines[i + 1 :]:
        row = ln.strip()
        if len(row) == 36 and row.isalpha():
            rows.append(row)
        elif rows:
            break
        if len(rows) == 13:
            break
    assert len(rows) == 13, rows
    return rows


def main(kupin_txt, reeds_txt):
    out = {
        "_source": "Rebuilt by code/extract_excerpts.py from the fetched sources. T1: Kupin 2014 "
        "p. 532, Sloane 8 ff. 102v-103r, first six rows as printed ('?' = illegible; 'ÿ' read "
        "as y). T5: Reeds 1998 p. 8, his transcription of T5 'Leo', first 13 rows.",
        "T1_sloane8_kupin": kupin_t1(kupin_txt),
        "T5_reeds1998": reeds_t5(reeds_txt),
    }
    (ROOT / "data").mkdir(exist_ok=True)
    json.dump(out, open(ROOT / "data" / "manuscript_excerpts.json", "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
