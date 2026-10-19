"""What kinds of slips separate the witnesses of the position numbers?

Uses only the printed numbers, never the code words, so it is a check of the error
model of repair.py that is independent of the answers. For every paragraph, every pair
of six-number witnesses (Sloane main text, translation, Bodley braces, Taurus margin)
is compared and the difference classified:
  same
  numeral   one number differs, by a one-character Roman numeral edit
  count     the differences are all +1 or all -1 and form a block of positions
            (as when the composer or a copyist counted one letter too many or too few
            in one name, which shifts every position in a stretch of the joined names);
            tested on the positions, i.e. all numbers above some value shift, others not
  other
Control: the same classification for 100,000 pairs of random six-number lists with the
same lengths of names (one list printed, the other with each number replaced at random
with the probability observed among real pairs), seed 20261019.

Usage: witness_diffs.py. Writes results/witness_diffs.json.
"""

import itertools
import json
import random
from pathlib import Path

from repair import ITEMS, numeral_edits, to_roman, witness_lists
from soyga import norm

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261019


def classify(a, b):
    d = [y - x for x, y in zip(a, b, strict=True)]
    nz = [i for i, x in enumerate(d) if x]
    if not nz:
        return "same"
    if len(nz) == 1:
        i = nz[0]
        return "numeral" if b[i] in numeral_edits(to_roman(a[i])) else "other"
    if len({d[i] for i in nz}) == 1 and abs(d[nz[0]]) == 1:
        # a count slip shifts every position past some point: check against positions
        lo = min(a[i] for i in nz)
        unchanged = [a[i] for i in range(6) if not d[i]]
        if all(u < lo for u in unchanged) or all(u > max(a[i] for i in nz) for u in unchanged):
            return "count"
        if len(nz) >= 2:
            return "count_partial"
    return "other"


def main():
    rng = random.Random(SEED)
    pairs = []
    for it in ITEMS:
        ws = sorted({v for _s, v in witness_lists(it) if len(v) == 6})
        for a, b in itertools.combinations(ws, 2):
            pairs.append({"label": it["label"], "a": a, "b": b, "kind": classify(a, b)})
    kinds = {}
    for p in pairs:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    # control: random perturbation with the same per-number change rate
    diff_nums = [
        sum(x != y for x, y in zip(p["a"], p["b"], strict=True))
        for p in pairs
        if p["kind"] != "same"
    ]
    rate = sum(diff_nums) / (6 * len(diff_nums))
    ctl = {}
    n = 100000
    for _ in range(n):
        it = rng.choice(ITEMS)
        L = len(norm("".join(it["names"][0])))
        a = tuple(rng.randint(1, L) for _ in range(6))
        b = tuple(x if rng.random() > rate else rng.randint(1, L) for x in a)
        if a == b:
            continue
        k = classify(a, b)
        ctl[k] = ctl.get(k, 0) + 1
    tot = sum(ctl.values())
    out = {
        "seed": SEED,
        "pairs": pairs,
        "kinds": kinds,
        "control": {
            "n_changed_pairs": tot,
            "per_number_change_rate": round(rate, 3),
            "share": {k: round(v / tot, 4) for k, v in ctl.items()},
        },
    }
    json.dump(out, open(ROOT / "results" / "witness_diffs.json", "w"), indent=1)
    for p in pairs:
        if p["kind"] != "same":
            print(f"{p['label']:11s} {p['a']} {p['b']} {p['kind']}")
    print(kinds)
    print(out["control"])


if __name__ == "__main__":
    main()
