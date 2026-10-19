"""List the spellings of each Section 28 divine name found anywhere in Kupin's edition.

Rule, declared before use: a spelling counts as a variant of a name if, after folding
to the table alphabet, it is one letter edit (insert, delete, substitute) away from the
name at an inner position (not the first or last letter, so Latin case endings such as
spiritum/sanctum do not count), the name has at least 5 letters, and the variant occurs
at least twice on the Latin pages of the edition (pages headed "[Section N]" but not
"Translation", so English words do not count). All tokens are listed with counts; the
"admitted" list applies the rule.

Usage: name_variants.py KUPIN_TXT  -> data/name_variants.json
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

from soyga import norm

ROOT = Path(__file__).resolve().parent.parent


def ed1(a, b):
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b, strict=True)) == 1
    if len(a) > len(b):
        a, b = b, a
    return any(b[:i] + b[i + 1 :] == a for i in range(len(b)))


def inner(a, b):
    """True if the single edit between a and b is at an inner position."""
    return a[0] == b[0] and a[-1] == b[-1] and ed1(a[1:-1], b[1:-1])


def main(txt):
    pages = open(txt, encoding="utf-8").read().split("\f")
    latin = [p for p in pages if "[Section" in p[:400] and "Translation]" not in p[:400]]
    toks = Counter(norm(t) for p in latin for t in re.findall(r"[A-Za-z]+", p))
    items = json.load(open(ROOT / "data" / "section28.json"))["items"]
    out = {}
    for it in items:
        for nm in it["names"]:
            for w in nm:
                k = norm(w)
                if k in out:
                    continue
                near = {
                    t: c
                    for t, c in toks.most_common()
                    if len(t) >= 3 and t[0] == k[0] and ed1(t, k)
                }
                adm = [
                    t
                    for t, c in near.items()
                    if t != k and c >= 2 and len(k) >= 5 and t[-1] == k[-1] and inner(t, k)
                ]
                out[k] = {"counts": near, "admitted": adm}
    json.dump(
        {"_source": "Kupin 2014 text layer; see name_variants.py", "variants": out},
        open(ROOT / "data" / "name_variants.json", "w"),
        indent=1,
    )
    for k, v in out.items():
        if v["admitted"]:
            print(
                k,
                v["admitted"],
                {t: v["counts"][t] for t in [k, *v["admitted"]] if t in v["counts"]},
            )


if __name__ == "__main__":
    main(sys.argv[1])
