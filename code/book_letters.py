"""Does book N "show" the N-th letter? (v1.3; a check of Teker's observation)

Teker (2026; v1.6 section 5.1 and v1.7 supplement section 3) reports that in the book
paragraphs of Sections 26.2-26.8 ("seipsum primo ostendit postea <L1> ... et est <N> in
nativitate eiusdem ... per <L2> idem nomen notificatur") the second letter L2 is the N-th
letter of the 23-letter alphabet in 13 of 16 clear cases (books 5-23), the misses being m for
n, G for s and B for k. This script reads the same paragraphs from Kupin's text with its own
pattern and counts. The observation is Teker's; this is a reproduction only.

Usage: book_letters.py KUPIN_TXT. Writes results/book_letters.json.
"""

import json
import re
import sys
from pathlib import Path

from soyga import ALPHA

ROOT = Path(__file__).resolve().parent.parent
ORD = {
    "quart": 4, "quint": 5, "sext": 6, "septim": 7, "octav": 8, "non": 9, "decim": 10,
    "undecim": 11, "duodec": 12,
}


def booknum(tok):
    t = re.sub(r"[^A-Za-z0-9]", "", tok).lower()
    m = re.match(r"\d+", t)
    if m:
        return int(m.group(0))
    for k in sorted(ORD, key=len, reverse=True):
        if t.startswith(k):
            return ORD[k]
    return None


def main(txt):
    pages = open(txt, encoding="utf-8").read().split("\f")
    latin = [
        p for p in pages if re.search(r"\[Section 26\.[2-8]\]", p[:400])
        and "Translation" not in p[:400] and "....." not in p
    ]
    text = " ".join(re.sub(r"\[[^\]]*\]", " ", "\n".join(latin)).split())
    pat = (r"primo ostendit,?\s+postea\s+(\S+).{0,300}?et est\s+(\S+)\s+in\s+nativita\w*"
           r".{0,60}?\bper\s+(\S+)\s+(?:idem|id est|scilicet)")
    rows = []
    for m in re.finditer(pat, text, re.I):
        n = booknum(m.group(2))
        l2 = re.sub(r"[^A-Za-z]", "", m.group(3))
        want = ALPHA[n - 1] if n and 1 <= n <= 23 else None
        if len(l2) != 1:
            res = "unclear"
        else:
            got = l2.lower().replace("v", "u")
            res = "match" if got == want else "miss"
        rows.append({"book": n, "first_letter_shown": m.group(1).strip(".,;"), "second_letter": l2,
                     "nth_letter": want, "result": res})
    rows.sort(key=lambda r: r["book"] or 0)
    clear = [r for r in rows if r["result"] != "unclear"]
    out = {
        "_source": "Kupin 2014 text layer; see book_letters.py; observation: Teker 2026",
        "paragraphs": len(rows),
        "books": [r["book"] for r in rows],
        "clear": len(clear),
        "matches": sum(r["result"] == "match" for r in clear),
        "misses": [r for r in clear if r["result"] == "miss"],
        "unclear": [r for r in rows if r["result"] == "unclear"],
        "rows": rows,
    }
    (ROOT / "results" / "book_letters.json").write_text(json.dumps(out, indent=1) + "\n")
    print({k: out[k] for k in ("paragraphs", "books", "clear", "matches")})
    for r in out["misses"] + out["unclear"]:
        print(r)


if __name__ == "__main__":
    main(sys.argv[1])
