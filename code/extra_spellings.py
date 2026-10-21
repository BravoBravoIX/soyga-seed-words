"""Sensitivity check (v1.3): the error model with the spellings of Sections 26.2-26.8, 29, 30.

Pre-registered in prereg/v1.3-extra-spellings.md, committed before this script was first run
in scoring mode. A check alongside the original error model (repair.py), not a replacement:
repair.py, its data and results/repair.json are unchanged.

Teker (21 October 2026) points out that the 23 triads of Section 28 stand, in the same order,
in Section 29 (a litany of invocations, alphabetical by the superlative), Section 30
(observances for each name) and the book paragraphs of Sections 26.2-26.8. Those give further
attested spellings of the 69 names. Section 29 and 30 stop after book 20 (Fire).

Extraction (declared rules; Latin pages of Kupin's edition only; table of contents excluded;
square-bracketed editorial matter removed; a Bodley reading in braces after a name counts as a
second spelling at the same place):
  Section 29  Each invocation "O <superlative> ... nomen tuum / nomina tua X[, Y, Z], ut".
              Book = place in the 23-letter alphabet of the superlative's first letter.
              Three names -> names 1, 2, 3; two names -> names 2, 3 (the "fili et spiritus"
              invocations); one name -> the nearest of the book's three names (see below).
  Section 30  The first word of each paragraph, and a capitalised word followed by an
              observance verb (cogit, praecipit, precipit, exigit, iubet, obtinet, debet, debes,
              pertinet). Book: the text runs book by book (Libra is missing), so each word is
              matched against the names of the current book and the next three; a match in a
              later book moves on.
  26.2-26.8   Book segments start at the first anchor naming the book's number ("N liber super
              tria nomina", "in N casu", "dictum (est) N in radii", "et est N in nativitate").
              The triad printed under a book heading -> names 1, 2, 3 by position. Any other
              capitalised word right after "hoc nomen", "potest dici", "dici potest",
              "nuncupari", "nuncupetur", "non discrepo" or "vocari" -> the nearest of the
              segment's book's three names.
  Nearest: Levenshtein distance on the folded spelling, to the Section 28 spelling(s) of each
  name; accepted only if the distance is at most half the length of that spelling, strictly
  smaller than to the other candidate names, and no name of another book is strictly nearer;
  a word that is exactly the Section 28 spelling of another book's name (and not a spelling
  of this book's) is a cross-reference, not a variant.
  Anything not accepted is listed as unassigned, not guessed.

Variants: every extracted spelling of a name that differs from its Section 28 spelling(s) and
from the spellings name_variants.py already admits becomes one more admitted spelling of that
name, for that paragraph only (primary set: attested once is enough; secondary set: attested
at least twice in the places read; third set: the primary set plus three listed words placed
by hand, see LISTED). The repair search is otherwise exactly repair.py's: same
error model, same costs, same seed and the same 100,000 random words per paragraph.

Usage: extra_spellings.py KUPIN_TXT [--extract-only]
Writes data/extra_spellings.json (extraction) and results/extra_spellings.json (scores).
"""

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

import repair
from soyga import ALPHA, norm

ROOT = Path(__file__).resolve().parent.parent
ITEMS = repair.ITEMS
VERBS = r"(?:cogit|praecipit|precipit|exigit|iubet|obtinet|debet|debes|pertinet)"
TRIGGERS = r"(?:hoc nomen|potest dici|dici potest|nuncupari|nuncupetur|non discrepo|vocari)"
ORD = {
    "quart": 4, "quint": 5, "sext": 6, "septim": 7, "octav": 8, "non": 9, "decim": 10,
    "undecim": 11, "duodec": 12,
}


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


BASE = {(it["n"], k): {norm(nm[k]) for nm in it["names"]} for it in ITEMS for k in range(3)}
ADMITTED = {
    (it["n"], k): {a for nm in it["names"] for a in repair.VARIANTS.get(norm(nm[k]), {}).get("admitted", [])}
    for it in ITEMS
    for k in range(3)
}


def nearest(word, books):
    """(book, k, distance) of the strictly nearest name among the given books, or None."""
    w = norm(word)
    books = [b for b in books if 1 <= b <= 23]
    others = [(b, k) for b in range(1, 24) if b not in books for k in range(3)]
    inbook = any(w in BASE[(b, k)] | ADMITTED[(b, k)] for b in books for k in range(3))
    if not inbook and any(w in BASE[o] for o in others):
        return None  # exactly another book's name: a cross-reference
    ds = sorted(
        min((lev(w, s), len(s)) for s in BASE[(b, k)]) + (b, k) for b in books for k in range(3)
    )
    if not ds or 2 * ds[0][0] > ds[0][1] or (len(ds) > 1 and ds[1][0] == ds[0][0]):
        return None
    if any(lev(w, s) < ds[0][0] for o in others for s in BASE[o]):
        return None  # another book's name is nearer
    return ds[0][2], ds[0][3], ds[0][0]


def latin_text(pages, pat):
    keep = [
        p for p in pages if re.search(pat, p[:400]) and "Translation" not in p[:400]
        and "....." not in p
    ]
    return "\n".join(keep)


def clean(s):
    return re.sub(r"\[[^\]]*\]", " ", s)


def split_alts(s):
    """'Elii {Ely}' -> ['Elii', 'Ely']; 'Agathabay{Agatabay}' -> both."""
    return [w for w in re.findall(r"[A-Za-z]+", s)]


def ext29(pages, rec, unassigned):
    txt = " ".join(latin_text(pages, r"\[Section 29\]").split())
    for chunk in re.split(r"\bO\s+(?=[a-z])", txt)[1:]:
        sup = chunk.split()[0]
        book = ALPHA.index(norm(sup)[0]) + 1
        m = re.search(r"(?:nomen tuum|nomina tua)\]?\s+(.+?),?\s+ut\b", chunk)
        if not m:
            unassigned.append({"section": "29", "book": book, "text": f"O {sup}", "why": "no name"})
            continue
        names = [clean(x).strip() for x in m.group(1).split(",") if clean(x).strip()]
        ks = {3: [0, 1, 2], 2: [1, 2]}.get(len(names))
        for i, nm in enumerate(names):
            if ks:
                k, how = ks[i], f"{len(names)} names, place {i + 1}"
            else:
                hit = nearest(split_alts(nm)[0], [book])
                if not hit:
                    unassigned.append({"section": "29", "book": book, "word": nm, "why": "no near name"})
                    continue
                k, how = hit[1], "one name, nearest"
            for w in split_alts(nm):
                rec.append({"section": "29", "book": book, "k": k, "spelling": w, "how": how,
                            "context": f"O {sup}"})


def ext30(pages, rec, unassigned):
    txt = latin_text(pages, r"\[Section 30\]")
    cands = []
    for line in txt.split("\n"):
        m = re.match(r"^\s{2,}([A-Z][A-Za-z]+)(\{[A-Za-z]+\})?", line)
        if m:
            cands.append((m.group(1), m.group(2), "paragraph start"))
        for m in re.finditer(r"[.\]]\s+([A-Z][A-Za-z]+)(\{[A-Za-z]+\})?,?\s+" + VERBS + r"\b", line):
            cands.append((m.group(1), m.group(2), "word before observance verb"))
    book = 1
    for w, alt, how in cands:
        hit = nearest(w, range(book, book + 4))
        if not hit or hit[0] > 20:
            unassigned.append({"section": "30", "book_now": book, "word": w, "why": "no near name"})
            continue
        book = hit[0]
        for s in [w] + ([alt.strip("{}")] if alt else []):
            rec.append({"section": "30", "book": book, "k": hit[1], "spelling": s, "how": how,
                        "context": w})


def booknum(tok):
    t = re.sub(r"[^A-Za-z0-9]", "", tok).lower()
    m = re.match(r"\d+", t)
    if m:
        return int(m.group(0))
    for k in sorted(ORD, key=len, reverse=True):
        if t.startswith(k):
            return ORD[k]
    return None


def ext26(pages, rec, unassigned):
    raw = latin_text(pages, r"\[Section 26\.[2-8]\]")
    txt = " ".join(clean(raw).split())
    anchors = {}
    pats = [
        r"(\w+)\s+(?:liber\s+)?super\s+(?:hec\s+|haec\s+)?tria\s+nomina",
        r"\bin\s+(\S+)\s+casu",
        r"dictum\s+(?:est\s+)?(\S+)\s+in\s+radii",
        r"et\s+est\s+(\S+)\s+in\s+nativita",
    ]
    for p in pats:
        for m in re.finditer(p, txt, re.I):
            n = booknum(m.group(1))
            if n and 4 <= n <= 23 and (n not in anchors or m.start() < anchors[n]):
                anchors[n] = m.start()
    order = sorted(anchors.items(), key=lambda x: x[1])
    segs = []
    for i, (n, s) in enumerate(order):
        e = order[i + 1][1] if i + 1 < len(order) else len(txt)
        segs.append((n, s, e))
    for n, s, e in segs:
        seg = txt[s:e]
        h = re.match(r"\w+\s+(?:liber\s+)?super\s+(?:hec\s+|haec\s+)?tria\s+nomina\s+"
                     r"([A-Z]\w+),\s*([A-Z]\w+),\s*([A-Z]\w+)", seg, re.I)
        if h:
            for k in range(3):
                rec.append({"section": "26", "book": n, "k": k, "spelling": h.group(k + 1),
                            "how": "book heading triad", "context": "heading"})
        for m in re.finditer(TRIGGERS + r"\s+([A-Z][A-Za-z]*)(\s*\{[A-Za-z]+\})?", seg):
            w = m.group(1)
            hit = nearest(w, [n])
            if not hit:
                g = nearest(w, range(1, 24))
                unassigned.append({"section": "26", "book": n, "word": w, "why": "no near name in book",
                                   "nearest_any_book": g})
                continue
            alts = [w] + ([m.group(2).strip(" {}")] if m.group(2) else [])
            for a in alts:
                rec.append({"section": "26", "book": n, "k": hit[1], "spelling": a,
                            "how": "after " + m.group(0).split(m.group(1))[0].strip(),
                            "context": " ".join(m.group(0).split())})
    return [(n, s) for n, s, _ in segs]


def extract(txt):
    pages = open(txt, encoding="utf-8").read().split("\f")
    rec, un = [], []
    ext29(pages, rec, un)
    ext30(pages, rec, un)
    books26 = ext26(pages, rec, un)
    names = {}
    for it in ITEMS:
        for k in range(3):
            key = f"{it['n']}.{k + 1}"
            found = Counter(norm(r["spelling"]) for r in rec if r["book"] == it["n"] and r["k"] == k)
            admitted = ADMITTED[(it["n"], k)]
            new = {s: c for s, c in found.items() if s not in BASE[(it["n"], k)] and s not in admitted}
            names[key] = {
                "label": it["label"],
                "section28": sorted(BASE[(it["n"], k)]),
                "already_admitted": sorted(admitted),
                "found": dict(found),
                "new_primary": sorted(new),
                "new_secondary": sorted(s for s, c in new.items() if c >= 2),
            }
    return {
        "_source": "Kupin 2014 text layer; see extra_spellings.py",
        "books_found_in_26": [n for n, _ in books26],
        "records": rec,
        "unassigned": un,
        "names": names,
    }


# Third set (declared with the others): the primary set plus three words the rules above leave
# unassigned, placed as Teker (2026, v1.7 section 4) and the order of the book read them:
# book 23's Iaech and Lanay (26.8; names 1 and 3) and Ysiis (Venus, name 2; a Venus passage
# that stands inside the book 16 segment of the edition).
LISTED = {(23, 0): {"iaech"}, (23, 2): {"lanay"}, (17, 1): {"ysiis"}}


def extra_map(ex, which):
    out = {}
    src = "new_primary" if which == "primary_plus_listed" else which
    for key, v in ex["names"].items():
        n, k = (int(x) for x in key.split("."))
        out[(n, k - 1)] = set(v[src])
    if which == "primary_plus_listed":
        for key, extra in LISTED.items():
            out[key] = out.get(key, set()) | extra
    return out


def make_source_variants(extra):
    """repair.source_variants, with the extra spellings admitted for each name of each item."""

    def source_variants(it, maxc):
        base = {norm("".join(nm)) for nm in it["names"]}
        res = {0: set(base), 1: set(), 2: set()}
        sp1 = set()
        for nm in it["names"]:
            for k, w in enumerate(nm):
                alts = set(repair.VARIANTS.get(norm(w), {}).get("admitted", []))
                alts |= extra.get((it["n"], k), set())
                for alt in alts:
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

    return source_variants


def score(extra):
    """repair.main's loop, unchanged apart from the admitted spellings."""
    original = repair.source_variants
    repair.source_variants = make_source_variants(extra)
    try:
        rng = random.Random(repair.SEED)
        targets = [norm(it["target"]) for it in ITEMS]
        items = []
        for i, it in enumerate(ITEMS):
            R = repair.reachable(it)
            t = targets[i]
            cost = next((c for c in sorted(R) if t in R[c]), None)
            src = norm("".join(it["names"][0]))
            rand = ["".join(src[rng.randrange(len(src))] for _ in range(6)) for _ in range(100000)]
            p = {c: sum(r in R[c] for r in rand) / len(rand) for c in R}
            others = {c: sorted(o for j, o in enumerate(targets) if j != i and o in R[c]) for c in R}
            how = []
            if cost:
                lv, sv = repair.list_variants(it, cost), repair.source_variants(it, cost)
                for cl in range(cost + 1):
                    for s in sv[cost - cl]:
                        for pl in lv[cl]:
                            if max(pl) <= len(s) and "".join(s[q - 1] for q in pl) == t:
                                how.append({"numbers": pl, "numbers_cost": cl, "names_joined": s})
            items.append({
                "n": it["n"], "label": it["label"], "target": t, "least_cost": cost,
                "derivations_at_least_cost": how, "chance_random_word": p,
                "other_code_words_reached": others,
                "reachable_sizes": {c: len(R[c]) for c in R},
            })
            print(f"{it['n']:2d} {it['label']:11s} {t} cost={cost} p1={p[1]:.5f} p2={p[2]:.5f} "
                  f"others1={len(others[1])} others2={len(others[2])}", flush=True)
        return items
    finally:
        repair.source_variants = original


def main(txt, extract_only=False):
    ex = extract(txt)
    (ROOT / "data" / "extra_spellings.json").write_text(json.dumps(ex, indent=1) + "\n")
    for key, v in ex["names"].items():
        if v["new_primary"]:
            print(key, v["label"], v["section28"], "->", v["new_primary"], "(2+:", v["new_secondary"], ")")
    print("unassigned:", len(ex["unassigned"]))
    if extract_only:
        return
    orig = {r["n"]: r for r in json.load(open(ROOT / "results" / "repair.json"))["items"]}
    out = {"seed": repair.SEED, "prereg": "prereg/v1.3-extra-spellings.md", "sets": {}}
    for which in ("new_primary", "new_secondary", "primary_plus_listed"):
        print("==", which)
        items = score(extra_map(ex, which))
        four = {}
        for r in items:
            if r["label"] in ("Cancer", "Pisces", "Mercury", "Moon"):
                o = orig[r["n"]]
                c = r["least_cost"]
                four[r["target"]] = {
                    "least_cost": c, "original_least_cost": o["least_cost"],
                    "chance": r["chance_random_word"][c],
                    "original_chance": o["chance_random_word"][str(c)],
                    "derivations": len(r["derivations_at_least_cost"]),
                    "original_derivations": len(o["derivations_at_least_cost"]),
                }
        summ = {
            "exact_at_cost": {c: sum(r["least_cost"] is not None and r["least_cost"] <= c for r in items)
                              for c in (0, 1, 2)},
            "four_repairs": four,
            "max_chance_at_cost1_over_all_paragraphs": max(r["chance_random_word"][1] for r in items),
            "wrong_code_words_reached": {
                c: sum(len(r["other_code_words_reached"][c]) for r in items) for c in (0, 1, 2)
            },
            "wrong_code_words_detail": {
                r["label"]: r["other_code_words_reached"] for r in items
                if any(r["other_code_words_reached"][c] for c in (0, 1, 2))
            },
        }
        print(json.dumps(summ, indent=1))
        out["sets"][which] = {"summary": summ, "items": items}
    (ROOT / "results" / "extra_spellings.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], "--extract-only" in sys.argv)
