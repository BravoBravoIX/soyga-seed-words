"""Can the code words that the printed numbers miss be explained by ordinary
copying or counting slips, and is that better than chance?

Error model, declared before running (each step costs 1; at most 2 steps):
  N  numeral slip: one character inserted, deleted or changed (i, v, x) in one Roman
     numeral; or two adjacent numbers run together (as Latin 'x, v' for xv in Taurus);
     or one number of a list longer than six dropped; or one number added to a list of
     five (any value).
  S  spelling: one name replaced by a spelling admitted by name_variants.py (attested at
     least twice on the Latin pages, one inner letter different).
  C  counting slip: the composer skipped or double-counted one letter of the joined
     names, i.e. every position after some point is one too high or too low (modelled
     as one letter deleted from or duplicated in the joined names).
Starting points (cost 0): every printed witness of the numbers (Latin, translation,
Bodley braces, Taurus margin) and every spelling printed in Section 28.

For each paragraph: the least cost at which its code word is produced exactly, and the
chance that a random code word is produced at that cost or less. Random code words are
6 letters drawn from random positions of the paragraph's own names (so they have the
right letters); 100,000 per paragraph, seed 20261019. A second control uses the 22 other
code words.

Usage: repair.py. Writes results/repair.json.
"""

import json
import random
from functools import cache
from pathlib import Path

from soyga import norm

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261019
ITEMS = json.load(open(ROOT / "data" / "section28.json"))["items"]
VARIANTS = json.load(open(ROOT / "data" / "name_variants.json"))["variants"]
ROMAN = {"i": 1, "v": 5, "x": 10, "l": 50}


def parse_roman(s):
    if not s or any(c not in ROMAN for c in s):
        return None
    tot, prev = 0, 0
    for c in reversed(s):
        v = ROMAN[c]
        if v < prev:
            tot -= v
        else:
            tot += v
            prev = v
    return tot if 1 <= tot <= 40 else None


def to_roman(n):
    out = "x" * (n // 10)
    n %= 10
    out += {
        0: "",
        1: "i",
        2: "ii",
        3: "iii",
        4: "iiii",
        5: "v",
        6: "vi",
        7: "vii",
        8: "viii",
        9: "viiii",
    }[n]
    return out


@cache
def numeral_edits(s):
    """Values reachable by one character edit of a Roman numeral string."""
    out = set()
    for i in range(len(s) + 1):
        for c in "ivx":
            out.add(parse_roman(s[:i] + c + s[i:]))
    for i in range(len(s)):
        out.add(parse_roman(s[:i] + s[i + 1 :]))
        for c in "ivx":
            if c != s[i]:
                out.add(parse_roman(s[:i] + c + s[i + 1 :]))
    out.discard(None)
    out.discard(parse_roman(s))
    return out


def witness_lists(it):
    """(numeral strings, values) for every printed witness."""
    out = []
    if "latin_numerals" in it:
        strs = [s if parse_roman(s) else None for s in it["latin_numerals"]]
        out.append((tuple(strs), tuple(it["latin"])))
    for k in ("latin", "trans", "bodley", "margin"):
        v = it.get(k)
        if v is None:
            continue
        for pl in v if isinstance(v[0], list) else [v]:
            out.append((tuple(to_roman(n) for n in pl), tuple(pl)))
    return out


def list_variants(it, maxc):
    """{cost: set of 6-number tuples}."""
    res = {c: set() for c in range(maxc + 1)}
    frontier = {(s, v) for s, v in witness_lists(it)}
    seen = set()
    for cost in range(maxc + 1):
        for _s, v in frontier:
            if len(v) == 6:
                res[cost].add(v)
        if cost == maxc:
            break
        nxt = set()
        for s, v in frontier:
            n = len(v)
            for i in range(n):
                if s[i]:
                    for nv in numeral_edits(s[i]):
                        nxt.add((s[:i] + (to_roman(nv),) + s[i + 1 :], v[:i] + (nv,) + v[i + 1 :]))
            for i in range(n - 1):  # run together
                m = v[i] + v[i + 1]
                nxt.add((s[:i] + (to_roman(m),) + s[i + 2 :], v[:i] + (m,) + v[i + 2 :]))
            if n > 6:
                for i in range(n):
                    nxt.add((s[:i] + s[i + 1 :], v[:i] + v[i + 1 :]))
            if n == 5:
                for i in range(n + 1):
                    for val in range(1, 31):
                        nxt.add((s[:i] + (to_roman(val),) + s[i:], v[:i] + (val,) + v[i:]))
        frontier = {x for x in nxt if x not in seen}
        seen |= frontier
    # make costs cumulative-exclusive
    allv = set()
    for c in range(maxc + 1):
        res[c] -= allv
        allv |= res[c]
    return res


def source_variants(it, maxc):
    """{cost: set of joined-name strings}."""
    base = {norm("".join(nm)) for nm in it["names"]}
    res = {0: set(base), 1: set(), 2: set()}
    # spellings
    sp1 = set()
    for nm in it["names"]:
        for k, w in enumerate(nm):
            for alt in VARIANTS.get(norm(w), {}).get("admitted", []):
                nm2 = [norm(x) for x in nm]
                nm2[k] = alt
                sp1.add("".join(nm2))

    def slips(s):
        return {s[:i] + s[i + 1 :] for i in range(len(s))} | {
            s[:i] + s[i] + s[i:] for i in range(len(s))
        }

    c1 = set(sp1)
    for s in base:
        c1 |= slips(s)
    res[1] = c1 - res[0]
    if maxc >= 2:
        c2 = set()
        for s in res[1]:
            c2 |= slips(s)
        res[2] = c2 - res[0] - res[1]
    return res


def reachable(it, maxc=2):
    lv = list_variants(it, maxc)
    sv = source_variants(it, maxc)
    by_cost = {c: set() for c in range(maxc + 1)}
    for cl in range(maxc + 1):
        for cs in range(maxc + 1 - cl):
            c = cl + cs
            for src in sv[cs]:
                L = len(src)
                for pl in lv[cl]:
                    if max(pl) <= L:
                        by_cost[c].add("".join(src[p - 1] for p in pl))
    out, acc = {}, set()
    for c in range(maxc + 1):
        acc = acc | by_cost[c]
        out[c] = set(acc)
    return out


def main():
    rng = random.Random(SEED)
    targets = [norm(it["target"]) for it in ITEMS]
    out = {"seed": SEED, "items": []}
    for i, it in enumerate(ITEMS):
        R = reachable(it)
        t = targets[i]
        cost = next((c for c in sorted(R) if t in R[c]), None)
        src = norm("".join(it["names"][0]))
        rand = ["".join(src[rng.randrange(len(src))] for _ in range(6)) for _ in range(100000)]
        p = {c: sum(r in R[c] for r in rand) / len(rand) for c in R}
        others = {c: sum(o in R[c] for j, o in enumerate(targets) if j != i) for c in R}
        how = []
        if cost:
            lv, sv = list_variants(it, cost), source_variants(it, cost)
            for cl in range(cost + 1):
                for src in sv[cost - cl]:
                    for pl in lv[cl]:
                        if max(pl) <= len(src) and "".join(src[q - 1] for q in pl) == t:
                            how.append({"numbers": pl, "numbers_cost": cl, "names_joined": src})
        rec = {
            "n": it["n"],
            "derivations_at_least_cost": how,
            "label": it["label"],
            "target": t,
            "least_cost": cost,
            "chance_random_word": p,
            "other_code_words_reached": others,
            "reachable_sizes": {c: len(R[c]) for c in R},
        }
        out["items"].append(rec)
        print(
            f"{it['n']:2d} {it['label']:11s} {t} cost={cost} p0={p[0]:.5f} p1={p[1]:.5f} "
            f"p2={p[2]:.5f} others={others}"
        )
    need = [r for r in out["items"] if r["least_cost"]]
    joint = 1.0
    for r in need:
        joint *= max(r["chance_random_word"][r["least_cost"]], 1e-5)
    out["summary"] = {
        "exact_at_cost": {
            c: sum(r["least_cost"] is not None and r["least_cost"] <= c for r in out["items"])
            for c in (0, 1, 2)
        },
        "needing_repair": [r["label"] for r in need],
        "max_chance_at_cost1_over_all_paragraphs": max(
            r["chance_random_word"][1] for r in out["items"]
        ),
        "joint_chance_bound_for_repaired": joint,
        "note": "chances of 0 in 100,000 are bounded at 1e-5 in the joint figure",
    }
    print(out["summary"])
    json.dump(out, open(ROOT / "results" / "repair.json", "w"), indent=1)


if __name__ == "__main__":
    main()
