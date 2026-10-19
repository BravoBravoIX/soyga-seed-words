"""Reproduce Reeds's generation rule and Louv's f = V - 1 on all 36 tables.

1. f from the Section 18 verse: which offsets k give f = V - k (mod 23), and how often a
   random assignment of the same values to letters matches f at any offset (control).
2. Generate the 36 tables with our own code; compare cell by cell with independent
   implementations (Louv 2026 reproduction package tables; orey/book-of-soyga output).
3. Compare with the manuscript readings in print (Sloane 8 T1 rows 1-6, Kupin 2014;
   T5 rows 1-13, Reeds 1998): cell agreement, each cell also predicted from its own
   neighbours in the transcription (so a copying error counts once), and the same for
   the 35 other tables as controls.

Usage: reproduce.py LOUV_TABLE_DIR OREY_TABLES_TXT  (either may be '-' to skip)
Writes results/reproduce.json. Seed 20261019.
"""

import hashlib
import json
import random
import sys
from pathlib import Path

from soyga import ALPHA, F_REEDS, IDX, TABLES, V18, gen_table, make_f

ROOT = Path(__file__).resolve().parent.parent
SEED = 20261019


def offsets():
    hits = {k: sum(make_f(V18, k)[c] == F_REEDS[c] for c in ALPHA) for k in range(23)}
    rng = random.Random(SEED)
    vals = [V18[c] for c in ALPHA]
    best = []
    for _ in range(100000):
        rng.shuffle(vals)
        perm = dict(zip(ALPHA, vals, strict=True))
        best.append(max(sum(make_f(perm, k)[c] == F_REEDS[c] for c in ALPHA) for k in range(23)))
    return {
        "matches_by_offset": hits,
        "offsets_with_23": [k for k, v in hits.items() if v == 23],
        "control_shuffled_values": {
            "n": len(best),
            "mean_best": round(sum(best) / len(best), 2),
            "max_best": max(best),
            "n_reaching_23": best.count(23),
        },
    }


def local_check(rows, f=F_REEDS):
    """Predict each interior cell from its own neighbours in the transcription."""
    ok = tot = 0
    bad = []
    for r in range(len(rows)):
        for c in range(1, len(rows[r])):
            x = rows[r][c]
            w = rows[r][c - 1]
            nn = rows[r - 1][c] if r else w
            if "?" in (x, w, nn):
                continue
            tot += 1
            pred = ALPHA[(IDX[nn] + f[w]) % 23]
            if pred == x:
                ok += 1
            else:
                bad.append([r + 1, c + 1, x, pred])
    return ok, tot, bad


def compare(rows, table):
    ok = tot = 0
    diffs = []
    for r, row in enumerate(rows):
        for c, x in enumerate(row):
            if x == "?":
                continue
            tot += 1
            if x == table[r][c]:
                ok += 1
            else:
                diffs.append([r + 1, c + 1, x, table[r][c]])
    return ok, tot, diffs


def main(louv_dir, orey_txt):
    out = {"seed": SEED, "f_from_verse": offsets()}
    tabs = {k + 1: gen_table(cw) for k, (_lab, cw) in enumerate(TABLES)}
    out["tables_sha256"] = hashlib.sha256(
        "\n".join("\n".join(t) for t in tabs.values()).encode()
    ).hexdigest()
    # independent implementations
    if louv_dir != "-":
        res = {}
        for p in sorted(Path(louv_dir).glob("T*.txt")):
            n = int(p.name[1:3])
            rows = [
                "".join(ch for ch in ln.lower() if ch in IDX)
                for ln in p.read_text().splitlines()
                if ln.strip() and not ln.startswith("#")
            ]
            rows = [r for r in rows if len(r) == 36]
            res[n] = sum(
                a == b
                for ra, rb in zip(rows, tabs[n], strict=False)
                for a, b in zip(ra, rb, strict=True)
            )
        out["vs_louv_tables"] = {
            "tables": len(res),
            "cells_equal": sum(res.values()),
            "cells": 1296 * len(res),
        }
    if orey_txt != "-":
        grids, cur = [], []
        for ln in Path(orey_txt).read_text().splitlines():
            parts = ln.split("-", 1)
            if len(parts) == 2 and parts[0].strip().isdigit():
                cur.append("".join(parts[1].split()))
                if len(cur) == 36:
                    grids.append(cur)
                    cur = []
        eq = sum(
            a == b
            for k, g in enumerate(grids)
            for ra, rb in zip(g, tabs[k + 1], strict=True)
            for a, b in zip(ra, rb, strict=True)
        )
        out["vs_orey_tables"] = {
            "tables": len(grids),
            "cells_equal": eq,
            "cells": 1296 * len(grids),
        }
    # manuscript readings
    ms = json.load(open(ROOT / "data" / "manuscript_excerpts.json"))
    for key, n in (("T1_sloane8_kupin", 1), ("T5_reeds1998", 5)):
        rows = [r.replace("v", "u") for r in ms[key]]  # v = u in the table alphabet
        ok, tot, diffs = compare(rows, tabs[n])
        lok, ltot, lbad = local_check(rows)
        controls = []
        for m in tabs:
            if m != n:
                controls.append(compare(rows, tabs[m])[0])
        out[key] = {
            "cells_equal_generated": [ok, tot],
            "differences": diffs,
            "local_rule_holds": [lok, ltot],
            "local_failures": lbad,
            "other_tables_cells_equal_max": max(controls),
        }
    json.dump(out, open(ROOT / "results" / "reproduce.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "f_from_verse"}, indent=1)[:3000])
    print(
        "offsets:",
        out["f_from_verse"]["offsets_with_23"],
        out["f_from_verse"]["control_shuffled_values"],
    )


if __name__ == "__main__":
    main(*sys.argv[1:3])
