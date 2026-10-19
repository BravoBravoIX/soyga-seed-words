"""Reproduce the code-word derivation of Section 28 (Ivezaj 2026, Louv 2026,
Teker 2026) from our own transcription, with controls.

Each of the 23 paragraphs gives position numbers; the code word is the letters at
those positions in the three divine names of the book, joined (Bodley marginal note:
"count those letters in the three names of the first book, and so for the others").

Readings (declared before scoring, following Teker 2026 Table 6):
  A_latin  position numbers as printed in the Latin text, main spellings
  A_trans  numbers as given in Kupin's translation, main spellings
  B        any printed witness (Latin, translation, Bodley braces, Taurus margin) and
           any spelling printed in Section 28 (main or Bodley)
Score: letters right (best option per paragraph, compared position by position for
6-number lists) and exact words.
Controls: (1) wrong book: each paragraph scored against the 22 other books' names;
(2) 100,000 random one-to-one pairings of name triples with paragraphs.

Usage: sec28.py. Writes results/sec28.json. Seed 20261019.
"""

import json
import random
from pathlib import Path

from soyga import norm

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261019
ITEMS = json.load(open(ROOT / "data" / "section28.json"))["items"]


def lists(it, which):
    out = []
    keys = {
        "A_latin": ["latin"],
        "A_trans": ["trans_or_latin"],
        "B": ["latin", "trans", "bodley", "margin"],
    }[which]
    for k in keys:
        if k == "trans_or_latin":
            v = it.get("trans", it["latin"])
        else:
            v = it.get(k)
        if v is None:
            continue
        out.extend(v if isinstance(v[0], list) else [v])
    return out


def spellings(it, which):
    return it["names"][:1] if which.startswith("A") else it["names"]


def apply(src, pl):
    return "".join(src[p - 1] if 0 < p <= len(src) else "?" for p in pl)


def score(target, src, pls):
    best = 0
    for pl in pls:
        got = apply(src, pl)
        if len(got) == len(target):
            s = sum(a == b for a, b in zip(got, target, strict=True))
        else:  # a list of the wrong length: best aligned window of 6, or 6-of-n
            s = max(
                (
                    sum(a == b for a, b in zip(got[i : i + 6], target, strict=False))
                    for i in range(max(1, len(got) - 5))
                ),
                default=0,
            )
        best = max(best, s)
    return best


def item_score(it, names_list, which):
    t = norm(it["target"])
    return max(score(t, norm("".join(nm)), lists(it, which)) for nm in names_list)


def main():
    rng = random.Random(SEED)
    out = {"seed": SEED, "readings": {}}
    for which in ("A_latin", "A_trans", "B"):
        per = [item_score(it, spellings(it, which), which) for it in ITEMS]
        wrong = []
        for i, it in enumerate(ITEMS):
            others = [
                item_score(it, spellings(o, which), which) for j, o in enumerate(ITEMS) if j != i
            ]
            wrong.append(sum(others) / len(others))
        # random pairings
        n = 100000
        mat = [[item_score(it, spellings(o, which), which) for o in ITEMS] for it in ITEMS]
        tot = []
        idx = list(range(len(ITEMS)))
        for _ in range(n):
            rng.shuffle(idx)
            tot.append(sum(mat[i][idx[i]] for i in range(len(ITEMS))))
        real = sum(per)
        out["readings"][which] = {
            "letters": real,
            "of": 6 * len(ITEMS),
            "exact_words": sum(s == 6 for s in per),
            "per_item": {it["label"]: s for it, s in zip(ITEMS, per, strict=True)},
            "wrong_book_mean_letters": round(sum(wrong), 1),
            "random_pairings": {
                "n": n,
                "mean": round(sum(tot) / n, 1),
                "max": max(tot),
                "n_ge_real": sum(x >= real for x in tot),
            },
        }
        r = out["readings"][which]
        print(
            which,
            r["letters"],
            "/",
            r["of"],
            "exact",
            r["exact_words"],
            "wrong-book",
            r["wrong_book_mean_letters"],
            "random",
            r["random_pairings"],
        )
        print("   misses:", {k: v for k, v in r["per_item"].items() if v < 6})
    json.dump(out, open(ROOT / "results" / "sec28.json", "w"), indent=1)


if __name__ == "__main__":
    main()
