"""Cancer (ISIAPO): do the two copies of the numbers differ by the one-s / two-s count?

Added in v1.2, after the v1.0 results (so this is an observation made after the fact,
tested here, not a prediction). The Bodley list 4, 15, 4, 5, 7, 11 gives ISIAPO exactly on
"Mesias" (Messias with one s). This script asks how the Sloane main-text list relates to it.

Sloane main text, as read by Teker (2026, Table 6): 4, 16, 2, 6, 8, 12 (Kupin marks the
Latin as uncertain: 'iiii, xvi, iii, [? could be xviiii] ii vi, viii, xii'; Teker drops the
doubtful iii). Aligned position by position with the Bodley list.

Two checks:
  1. Letter by letter: which spelling each copy's number reads the code-word letter on.
  2. Chance: if a copyist changed numbers at random, how often would at least as many of the
     changed numbers be exactly one higher than Bodley's? Each changed number is replaced by
     a random other position in the joined names (1..16), 1,000,000 trials, seed 20261019.

Usage: cancer_copies.py. Writes results/cancer_copies.json.
"""

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261019
TRIALS = 1_000_000

TARGET = "isiapo"
ONE_S = "mesiaspantonhos"    # Mesias Panton Hos
TWO_S = "messiaspantonhos"   # Messias Panton Hos, as the edition spells it
BODLEY = [4, 15, 4, 5, 7, 11]
SLOANE = [4, 16, 2, 6, 8, 12]  # Teker's reading of the main text


def read(names, n):
    return names[n - 1] if 1 <= n <= len(names) else "?"


def main():
    rows = []
    for i, (b, s) in enumerate(zip(BODLEY, SLOANE)):
        rows.append({
            "letter": TARGET[i],
            "bodley": b, "bodley_on_one_s": read(ONE_S, b), "bodley_on_two_s": read(TWO_S, b),
            "sloane": s, "sloane_on_one_s": read(ONE_S, s), "sloane_on_two_s": read(TWO_S, s),
            "sloane_minus_bodley": s - b,
        })
    changed = [r for r in rows if r["sloane_minus_bodley"] != 0]
    plus_one = sum(r["sloane_minus_bodley"] == 1 for r in changed)

    rng = random.Random(SEED)
    hits = 0
    n_pos = len(TWO_S)
    for _ in range(TRIALS):
        k = 0
        for r in changed:
            v = rng.randint(1, n_pos - 1)
            if v >= r["bodley"]:
                v += 1  # a random position other than Bodley's
            k += v == r["bodley"] + 1
        hits += k >= plus_one

    out = {
        "seed": SEED,
        "trials": TRIALS,
        "sloane_reading": "Teker 2026, Table 6 (main text)",
        "rows": rows,
        "bodley_exact_on_one_s": sum(r["bodley_on_one_s"] == r["letter"] for r in rows),
        "sloane_exact_on_two_s": sum(r["sloane_on_two_s"] == r["letter"] for r in rows),
        "changed_positions": len(changed),
        "changed_exactly_plus_one": plus_one,
        "chance_at_least_as_many_plus_one": hits / TRIALS,
        "first_number_both_copies": [rows[0]["bodley"], rows[0]["sloane"]],
        "position_4": {"one_s": read(ONE_S, 4), "two_s": read(TWO_S, 4)},
    }
    (ROOT / "results" / "cancer_copies.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()
