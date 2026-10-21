"""How does the edition spell Messias? (v1.3; a check of Teker's count, 21 October 2026)

Teker (2026, v1.7 supplement, section 5) counts "Messias" 10 times and "Messyas" 7 times in
Kupin's transcription, and the one-s form "Mesias" never, so the ISIAPO repair is a counting
slip, not a spelling. This script counts every token that begins "mes" and is within two
letter edits of "messias", after folding to the table alphabet, on the Latin pages of the
edition (the same pages name_variants.py reads) and, separately, on every page.

Usage: messias_count.py KUPIN_TXT. Writes results/messias_count.json.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

from soyga import norm

ROOT = Path(__file__).resolve().parent.parent


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def count(pages):
    toks = Counter(norm(t) for p in pages for t in re.findall(r"[A-Za-z]+", p))
    return {t: c for t, c in sorted(toks.items()) if t.startswith("mes") and lev(t, "messias") <= 2}


def main(txt):
    pages = open(txt, encoding="utf-8").read().split("\f")
    latin = [p for p in pages if "[Section" in p[:400] and "Translation]" not in p[:400]]
    lat, every = count(latin), count(pages)
    one_s = {t: c for t, c in every.items() if t.startswith("mes") and not t.startswith("mess")}
    out = {
        "_source": "Kupin 2014 text layer; see messias_count.py",
        "latin_pages": lat,
        "all_pages": every,
        "one_s_forms_anywhere": one_s,
        "messias_latin": lat.get("messias", 0),
        "messyas_latin": lat.get("messyas", 0),
        "mesias_latin": lat.get("mesias", 0),
        "mesias_anywhere": every.get("mesias", 0),
    }
    (ROOT / "results" / "messias_count.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
