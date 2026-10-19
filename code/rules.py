"""Is there a rule behind the position numbers, or were the code words chosen?

Data: the 23 paragraphs with the numbers and spelling that give the code word exactly
(repair.py, least-cost derivation; the first one listed when there are several).

Tests, each against a stated null (seed 20261019):
 T1 vowels: share of vowels (a e i o u y) in the code words, against six letters taken
    at random positions of the same names (100,000 draws of all 23).
 T2 three names: how many code words take letters from all three names, against random
    positions.
 T3 occurrence: where a letter occurs more than once in the names, how often the first
    occurrence is used, against choosing an occurrence at random (exact expectation).
 T4 order: how many of the 115 steps between successive positions go up, against random.
 T5 compact rules, fitted per paragraph, scored by exact code words, each against the
    same rule applied to the names of the other 22 paragraphs (the code word moved to a
    wrong book) so that the rule's freedom is measured:
      R1 arithmetic progression p_k = a + b k (mod L), a, b free
      R2 the same with one step b shared by all paragraphs (leave-one-out: b fitted on
         the other 22 paragraphs)
      R3 positions from the letter values (Section 18) of the code word's own letters
         counted on from the previous position: p_k = p_(k-1) + V(c_(k-1)) (mod L),
         p_0 free
      R4 the same with alphabet numbers (a = 1 ... z = 23)
      R5 positions counted with a fixed stride s through the names, taking the next
         occurrence of each needed letter (a 'reading' of the names), s and the start
         free; scored on the printed positions, not the word (the word alone is
         trivially reachable with s = 1)
 Leave-one-out applies to the shared parameter of R2 only; R1, R3-R5 have per-paragraph
 parameters and are judged by the wrong-book control.

Usage: rules.py. Writes results/rules.json.
"""

import json
import random
from pathlib import Path

from soyga import ALPHA, IDX, V18, norm

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261019
VOW = set("aeiouy")


def load():
    rep = json.load(open(ROOT / "results" / "repair.json"))["items"]
    items = json.load(open(ROOT / "data" / "section28.json"))["items"]
    data = []
    for it, r in zip(items, rep, strict=True):
        d = r["derivations_at_least_cost"]
        if d:
            pl, src = tuple(d[0]["numbers"]), d[0]["names_joined"]
        else:  # exact at cost 0: find the printed list and spelling
            t = r["target"]
            from repair import witness_lists

            found = None
            for nm in it["names"]:
                s = norm("".join(nm))
                for _st, v in witness_lists(it):
                    if len(v) == 6 and max(v) <= len(s) and "".join(s[p - 1] for p in v) == t:
                        found = (v, s)
                        break
                if found:
                    break
            pl, src = found
        lens = None
        for nm in it["names"]:
            if norm("".join(nm)) == src:
                lens = [len(norm(x)) for x in nm]
        if lens is None:  # a repaired spelling: take the main name lengths, adjusted
            lens = [len(norm(x)) for x in it["names"][0]]
            lens[-1] += len(src) - sum(lens)
        data.append(
            {"label": it["label"], "target": r["target"], "pos": pl, "src": src, "lens": lens}
        )
    return data


def which_name(p, lens):
    a = lens[0]
    b = a + lens[1]
    return 0 if p <= a else 1 if p <= b else 2


def t1_vowels(data, rng, n=100000):
    real = sum(c in VOW for d in data for c in d["target"])
    null = []
    for _ in range(n):
        null.append(
            sum(d["src"][rng.randrange(len(d["src"]))] in VOW for d in data for _k in range(6))
        )
    src_share = sum(sum(c in VOW for c in d["src"]) / len(d["src"]) for d in data) / len(data)
    return {
        "real": real,
        "of": 6 * len(data),
        "null_mean": round(sum(null) / n, 1),
        "null_max": max(null),
        "p": (sum(x >= real for x in null) + 1) / (n + 1),
        "vowel_share_of_names": round(src_share, 3),
    }


def t2_three(data, rng, n=100000):
    real = sum(len({which_name(p, d["lens"]) for p in d["pos"]}) == 3 for d in data)
    null = []
    for _ in range(n):
        null.append(
            sum(
                len({which_name(rng.randint(1, len(d["src"])), d["lens"]) for _k in range(6)}) == 3
                for d in data
            )
        )
    return {
        "real": real,
        "of": len(data),
        "null_mean": round(sum(null) / n, 2),
        "p_ge": (sum(x >= real for x in null) + 1) / (n + 1),
        "p_le": (sum(x <= real for x in null) + 1) / (n + 1),
    }


def t3_first(data, rng, n_sim=100000):
    obs = exp = n = 0
    ks = []
    for d in data:
        for c, p in zip(d["target"], d["pos"], strict=True):
            occ = [i + 1 for i, x in enumerate(d["src"]) if x == c]
            if len(occ) > 1:
                n += 1
                obs += p == occ[0]
                exp += 1 / len(occ)
                ks.append(len(occ))
    sims = [sum(rng.random() < 1 / k for k in ks) for _ in range(n_sim)]
    return {
        "letters_with_choice": n,
        "first_occurrence_used": obs,
        "expected_if_random": round(exp, 1),
        "p_ge": (sum(x >= obs for x in sims) + 1) / (n_sim + 1),
    }


def t4_up(data, rng, n=100000):
    real = sum(b > a for d in data for a, b in zip(d["pos"], d["pos"][1:], strict=False))
    null = []
    for _ in range(n):
        tot = 0
        for d in data:
            ps = [rng.randint(1, len(d["src"])) for _k in range(6)]
            tot += sum(b > a for a, b in zip(ps, ps[1:], strict=False))
        null.append(tot)
    return {
        "real": real,
        "of": 5 * len(data),
        "null_mean": round(sum(null) / n, 1),
        "p_ge": (sum(x >= real for x in null) + 1) / (n + 1),
        "p_le": (sum(x <= real for x in null) + 1) / (n + 1),
    }


def r1(src, t):
    L = len(src)
    return any(
        "".join(src[(a + b * k) % L] for k in range(6)) == t for a in range(L) for b in range(L)
    )


def r1_with_b(src, t, b):
    L = len(src)
    return any("".join(src[(a + b * k) % L] for k in range(6)) == t for a in range(L))


def r_values(src, t, val):
    L = len(src)
    for p0 in range(L):
        ps = [p0]
        for k in range(1, 6):
            ps.append((ps[-1] + val[t[k - 1]]) % L)
        if "".join(src[p] for p in ps) == t:
            return True
    return False


def r5(src, t, pos):
    L = len(src)
    want = [q - 1 for q in pos]
    for s in range(1, L + 1):
        for start in range(L):
            p, got = start, []
            for c in t:
                for _k in range(L):
                    if src[p % L] == c:
                        break
                    p += s
                else:
                    break
                got.append(p % L)
                p += s
            if got == want:
                return True
    return False


def t5(data):
    alpha_num = {c: IDX[c] + 1 for c in ALPHA}
    rules = {
        "R1_progression": r1,
        "R3_values_V18": lambda s, t: r_values(s, t, V18),
        "R4_alphabet_numbers": lambda s, t: r_values(s, t, alpha_num),
    }
    out = {}
    for name, f in rules.items():
        real = [d["label"] for d in data if f(d["src"], d["target"])]
        wrong = sum(f(o["src"], d["target"]) for d in data for o in data if o is not d)
        out[name] = {
            "exact": len(real),
            "which": real,
            "wrong_book_rate_per_paragraph": round(wrong / (len(data) - 1), 2),
        }
    real = [d["label"] for d in data if r5(d["src"], d["target"], d["pos"])]
    # control: the same word with each letter's occurrence chosen at random (200 draws)
    rng = random.Random(SEED + 5)
    expected = 0.0
    for d in data:
        occ = [[i + 1 for i, x in enumerate(d["src"]) if x == c] for c in d["target"]]
        draws = [tuple(rng.choice(o) for o in occ) for _ in range(200)]
        expected += sum(r5(d["src"], d["target"], dr) for dr in draws) / len(draws)
    out["R5_stride_reading_positions"] = {
        "exact": len(real),
        "which": real,
        "expected_with_random_occurrences": round(expected, 1),
    }
    # R2: one shared step, leave one out
    hits = []
    for i, d in enumerate(data):
        best_b, best_n = None, -1
        for b in range(1, 25):
            nb = sum(r1_with_b(o["src"], o["target"], b) for j, o in enumerate(data) if j != i)
            if nb > best_n:
                best_b, best_n = b, nb
        hits.append(r1_with_b(d["src"], d["target"], best_b))
    out["R2_shared_step_loo"] = {
        "exact": sum(hits),
        "which": [d["label"] for d, h in zip(data, hits, strict=True) if h],
    }
    return out


def main():
    rng = random.Random(SEED)
    data = load()
    out = {
        "seed": SEED,
        "data": data,
        "T1_vowels": t1_vowels(data, rng),
        "T2_three_names": t2_three(data, rng),
        "T3_first_occurrence": t3_first(data, rng),
        "T4_steps_up": t4_up(data, rng),
        "T5_rules": t5(data),
    }
    json.dump(out, open(ROOT / "results" / "rules.json", "w"), indent=1)
    for k, v in out.items():
        if k.startswith("T"):
            print(k, v)


if __name__ == "__main__":
    main()
