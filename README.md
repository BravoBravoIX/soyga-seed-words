# The Book of Soyga: how the 36 tables' seed words were chosen

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23470965.svg)](https://doi.org/10.5281/zenodo.23470965)

The *Book of Soyga* (*Aldaraia*) is an anonymous sixteenth-century Latin book of magic, known
from two manuscripts: British Library Sloane MS 8 and Bodleian MS Bodley 908. John Dee owned
a copy. It ends with 36 tables of 36 × 36 letters. Each table grows from a six-letter "seed",
or code word, written down its left margin.

This study asks where those 36 code words came from. It reproduces the published answers,
explains the four code words that were still unexplained, and tests whether any compact rule
lies behind the numbers the book uses to spell them.

This is a study of how a text was made. It is not a decipherment: the tables were broken by
Jim Reeds in 1998. Where the evidence is short of proof, this README says "the evidence weighs
toward".

October 2026. CPU only, Python standard library only; the whole analysis reruns in about a
minute and a half.

**Archived on Zenodo** with its paper, code, data and results: [doi:10.5281/zenodo.23470965](https://doi.org/10.5281/zenodo.23470965) (this DOI always opens the latest version; see How to cite at the end).

**The paper:** [`paper/soyga-seed-words.pdf`](paper/soyga-seed-words.pdf) (working paper, 5 pages:
abstract, method, results, discussion and references; built from `paper/soyga-seed-words.typ`
by `paper/build.sh`). The README below covers the same ground in more detail.

## In short

| Question | Answer | How firm |
|---|---|---|
| Do the tables follow Reeds's rule, with Louv's step function f = V − 1? | Yes. Our own generator gives all 36 tables, equal in all 46,656 cells to two independent implementations | f fits all 23 letters at offset 1 only; 100,000 shuffles of the values never fit more than 11 |
| Where do the 36 code words come from? | 12 are the reverses of tables 1–12, one is MOYSES, and 23 are spelled out by position numbers in the book's three divine names | The 23 spellings: 19 of 23 exact as printed (as Teker found); random pairings of names and paragraphs reach at most 69 of 138 letters, against 131 |
| Can the last four (ISIAPO, ARICAA, REUELA, UISEUA) be explained? | Yes. Each is one ordinary copying or counting slip away, under one error model written down before scoring | Chance that one slip turns the same names into a random word: 0.00044, 0.00005, 0.00002 and 0.00004 |
| Does the error model let in wrong answers? | No. No paragraph produces any of the other 22 code words, even with two slips | 0 of 22 × 23 cross-pairings |
| Are those kinds of slip real? | Yes. The copies of the numbers disagree with each other by exactly these two kinds of slip, far more often than random lists | One-numeral slips 28 % against 8 %; counting slips 17 % against 0.2 % |
| Is there a rule that produces the positions (or the words) from the names? | None found. The words look chosen: vowel-rich, and drawing on all three names | Vowels 82 of 138 against 61.5 expected (p ≈ 0.0004); five rule families fail |

## 1. The problem

**The tables.** Reeds (1998, 2006) showed how each table is built. The left column is the
code word followed by its reverse, repeated down the 36 rows. Every other cell is the letter
above it moved on through the 23-letter alphabet by a step that depends on the letter to its
left. Reeds found the step for each letter, f, by working it out from the tables; he called
the numbers in the book's text that seemed to go with the code words "in unknown relation" to
them.

**The step function.** Jason Louv (2026) found f in the book itself: a Latin verse in
Section 18 gives a number V to each letter, and f = V − 1 (mod 23).

**The code words.** That left the seeds. Section 28 of the book has 23 short paragraphs, one
for each of the twelve signs, the seven planets and the four elements. Each gives a short list
of numbers, mostly six, and each book of the work has three divine names (for example Agla,
Primogenitus, On). A note in the Bodley margin says to count those letters in the three names
of each book. Ilir Ivezaj (2026) and Louv (2026) read the code words this way. Onur Teker
(preprint, Zenodo, 17 October 2026) did it systematically, with controls, across every printed
copy of the numbers and every printed spelling of the names: **19 of 23 code words come out
exactly**, 131 of 138 letters. Four stayed open: **ISIAPO** (Cancer), **ARICAA** (Pisces),
**REUELA** (Mercury) and **UISEUA** (Moon).

**The questions**, made checkable:
1. Do the printed numbers, applied to the joined three names, give each code word? Where they
   do not, is there a repair that is plausible as a copying slip and better than chance?
2. Is there a rule that produces the numbers, or the words, without being told the word?

## 2. Sources

None of the third-party texts or tables is included here (see Licensing).
`scripts/fetch_sources.sh` downloads them from where their owners publish them, and the code
reads them locally.

| Source | Used for |
|---|---|
| Jane Kupin (2014), *The Book of Soyga*, Latin transcription and English translation (copy in the orey/book-of-soyga repository) | Section 18 verse; Section 28 numbers and names; the six rows of table 1 printed from Sloane 8; the spellings of each name across the book |
| Jim Reeds (1998), "John Dee and the Magic Tables in the Book of Soyga", preprint (same repository) | the generation rule; the code words (his Table I); his transcription of 13 rows of table 5 |
| orey/book-of-soyga (GitHub), generated tables | an independent implementation to compare against |
| Louv (2026) reproduction package, Zenodo 10.5281/zenodo.20696278 | a second independent implementation |
| Teker (2026) preprint, supplement and code, Zenodo 10.5281/zenodo.23431833 | comparison only; the pipeline does not read them |

Our own data, written by hand from Kupin's edition: `data/section28.json`, the position numbers
and names of the 23 paragraphs, with every printed copy (Sloane main text, Kupin's translation
where it reads the Latin differently, the Bodley variants printed in braces, and the Taurus
margin) and the Roman numerals as printed. Notes record where the editor is unsure.

## 3. Method

All random processes use the seed 20261019.

| Script | What it does |
|---|---|
| `code/soyga.py` | The alphabet, the Section 18 verse parsed line by line, Reeds's f, the generator, the 36 code words |
| `code/extract_excerpts.py` | Pulls the two printed manuscript excerpts out of the fetched PDFs' text |
| `code/reproduce.py` | f against V at all 23 offsets, with 100,000 shuffled value tables; our 36 tables against Louv's and orey's; the manuscript excerpts cell by cell, with the other 35 tables as controls |
| `code/sec28.py` | The code words from the printed numbers (as printed in Latin; as translated; any printed copy), with two controls: each paragraph scored against the 22 wrong books' names, and 100,000 random pairings of names with paragraphs |
| `code/name_variants.py` | Every spelling of each divine name on the Latin pages of the edition. Declared rule: one inner letter different, occurring at least twice |
| `code/repair.py` | The slip model; the least number of slips per paragraph; chance for 100,000 random words per paragraph; the other code words as a second control |
| `code/witness_diffs.py` | The kinds of slip between the printed copies of the numbers, with no code words used, against random lists |
| `code/cancer_copies.py` | (v1.2) Cancer: the Sloane and Bodley copies of the numbers read letter by letter on "Messias" and "Mesias", with a chance figure |
| `code/rules.py` | The tests of question 2 |

**The error model**, written into `code/repair.py` before any scoring was run. Each step costs
one, at most two in all:
- **numeral slip**: one character added, dropped or changed in one Roman numeral (so xvi can
  become vi or xvii); or two numbers run together (as the Latin "x, v" that the translation
  reads as xv); or one number dropped from a list longer than six, or added to a list of five;
- **spelling**: one name replaced by a spelling the book itself uses elsewhere (the declared
  rule above);
- **counting slip**: one letter of the joined names skipped or counted twice, so every position
  after that point is one too high or too low.

Starting points, at no cost: every printed copy of the numbers and every spelling printed in
Section 28.

**Chance.** For each paragraph, 100,000 random six-letter "code words" are drawn from random
positions of the same three names (so they use the right letters), and we count how many the
same number of slips would also produce. The second control asks whether any paragraph's
slips produce one of the other 22 real code words.

## 4. Results

### Reeds's rule and Louv's f, reproduced (`results/reproduce.json`)

- f = V − 1 (mod 23) holds for all 23 letters at offset 1, and at no other offset. Shuffled
  value tables (100,000) fit at most 11 letters at any offset.
- Our 36 tables equal Louv's and orey's in all 46,656 cells.
- The rule fits the only manuscript cells in print that we could find:
  - Sloane 8 table 1, rows 1–6 (Kupin p. 532): 206 of 215 legible cells; 7 of the 9 misses
    are q read as g, as Ivezaj noted;
  - Reeds's table 5, rows 1–13: 466 of 468;
  - no other table comes close (at most 104 and 282 cells).

### The 36 code words

- **12 are reverses.** Tables 13–24 repeat the twelve signs, and their code words are those of
  tables 1–12 written backwards (NISRAM / MARSIN and so on). The text says so.
- **MOYSES** heads the last table, "Magistri", the practitioner's own (the closing paragraph;
  as Ivezaj noted).
- **The other 23** are spelled out in Section 28 by position numbers in the three divine names
  of each book (`results/sec28.json`):

| Reading of the numbers | Letters (of 138) | Exact words (of 23) | Wrong book, mean | Random pairings, max |
|---|---|---|---|---|
| as printed in the Latin | 114 | 13 | 13.3 | 55 |
| as given in Kupin's translation | 112 | 13 | 13.2 | 52 |
| any printed copy, any printed spelling | 131 | 19 | 17.6 | 69 |

None of 100,000 random pairings reaches the real score in any reading. Teker reports 115, 113
and 131; the small difference in the first two comes from how lists that are not six numbers
long are scored.

### The four that were open: one ordinary slip each (`results/repair.json`)

| Table | Code word | What gives it exactly | Kind of slip | Chance for a random word |
|---|---|---|---|---|
| Cancer | ISIAPO | the Bodley numbers 4, 15, 4, 5, 7, 11, counted on "Messias" with one s (Mesias Panton Hos; skipping any one of its first three letters gives the same) | counting | 0.00044 |
| Pisces | ARICAA | the printed numbers on Griszon Misericors **Agatay**, the book's usual spelling (7 times, against Agathay once); or Agathay with the last number 22 → 23 | spelling (or numeral) | 0.00005 |
| Mercury | REUELA | the printed numbers on Solus **Grisdecon** Agatabaii, the book's usual spelling (6 times, against Griisdecon once) | spelling | 0.00002 |
| Moon | UISEUA | the numbers 17, 13, 14, 10, 17, 16 with the last read **vi** for xvi | numeral | 0.00004 |

- With no slips, 19 paragraphs give their code word exactly; with at most one slip, all 23 do.
- The largest one-slip chance for any of the 23 paragraphs is 0.0027 (Taurus, which needs no
  slip at all).
- **No paragraph gives a wrong code word.** Under the same model, none of the 23 paragraphs
  produces any of the other 22 code words, even with two slips.

### Cancer: the two copies differ by the one-s count (v1.2; `results/cancer_copies.json`)

Added after v1.0, so it is an observation made after the fact, tested here, not a prediction.
Set side by side, position by position:

| Letter of ISIAPO | I | S | I | A | P | O |
|---|---|---|---|---|---|---|
| Bodley numbers (give ISIAPO on "Mesias") | 4 | 15 | 4 | 5 | 7 | 11 |
| Sloane main text (Teker's reading) | 4 | 16 | 2 | 6 | 8 | 12 |
| Sloane read on "Messias" (two s) | s | **s** | e | **a** | **p** | **o** |

- The Bodley numbers give all six letters on the one-s spelling.
- Where the Sloane copy differs (5 places), 4 of its numbers are exactly one higher than
  Bodley's, and each of those 4 gives the right letter on the two-s spelling "Messias". That
  is what a recount of those letters on "Messias" would produce. If a copyist had changed the
  numbers at random, 4 or more of 5 changes would be exactly one higher in about 1 trial in
  10,000 (0.000094; 1,000,000 trials).
- Both copies begin with 4 for the first I. Position 4 is I only on the one-s spelling (on
  "Messias" it is s), so even the Sloane copy keeps a trace of a one-s count.
- The third number (Sloane 2, Bodley 4) does not fit either spelling; the Sloane line is
  corrupt there (Kupin marks it uncertain).

So the copies themselves show the Cancer letters being counted on two spellings that differ
by one s. The evidence weighs toward the Bodley list being the original one-s count, and the
Sloane numbers a partial recount on "Messias". Teker (2026) reads the Sloane line the same
way but does not compare it with the Bodley numbers on the two spellings; we found this
comparison nowhere earlier.

### The copies of the numbers make the same slips (`results/witness_diffs.json`)

This check uses only the printed numbers, never the code words, so it tests the error model
independently of the answers. Where two printed copies of the same paragraph's numbers
disagree (18 pairs):
- 5 differ by one Roman-numeral slip (28 %, against 8 % for random lists with the same rate of
  change);
- 3 differ by a counting slip, a block of positions all one higher or lower (17 %, against
  0.2 %). Examples: Taurus, Bodley 8, 14, 2, 10, 4, 1 against 9, 15, 2, 11, 4, 1; Jupiter,
  Bodley 16, 14, 10, 20, 19, 6 against 17, 15, 11, 21, 20, 6.

So the two kinds of slip the repairs rely on are the kinds the scribes and the composer can be
seen making elsewhere in the same section.

### Is there a rule behind the positions? (`results/rules.json`)

Using the 23 position lists that give the code words exactly:
- **Vowels.** The code words are rich in vowels: 82 of 138 letters, against 61.5 expected from
  random positions in the same names (p ≈ 0.0004).
- **All three names.** 20 of 23 draw on all three names, against 15.1 expected (p ≈ 0.02).
- **Compact rules fail**, each judged against the same rule applied to the wrong book's names:
  - an arithmetic progression of positions: Saturn only (7, 9, 11, 13, 15, 17);
  - steps taken from the Section 18 letter values: none;
  - steps taken from the letters' places in the alphabet: none;
  - one step shared by all paragraphs, fitted on the other 22: none held out;
  - a fixed-stride reading through the names: 9 of 23, against 10.4 expected if each letter's
    position were picked at random among its occurrences.
- Two weaker tendencies are not significant: first occurrences used 42 times against 35.3
  expected (p ≈ 0.08); positions rising 60 of 115 steps against 54.4 (p ≈ 0.08).

## 5. Verdict

- **The selection of all 36 code words is accounted for**: 12 reverses, MOYSES, and 23 words
  spelled from the three divine names, 19 exactly as printed and 4 after one ordinary slip
  each. Each of the four repairs beats chance by three orders of magnitude or more, the model
  that allows them produces no wrong code word, and the same kinds of slip are seen among the
  printed copies themselves.
- **No rule that predicts the words from the names was found**, here or in Ahmadipour's tests.
  The evidence weighs toward free choice: the author picked a pronounceable six-letter word
  from the letters of all three names and wrote down where each letter sits. The numbers
  record that choice; no generator of positions lies behind them.

## 6. What is new, and what earlier work did

This study stands on the work of others:

- **Jim Reeds** (1998 preprint; 2006, in Clucas, ed., *John Dee: Interdisciplinary Studies in
  English Renaissance Thought*, Springer) broke the tables: the generation rule, the step
  function, and the list of code words.
- **Jane Kupin** (2014) published the Latin transcription and English translation that every
  number and name here is read from.
- **Jason Louv** (2026; Zenodo 10.5281/zenodo.20635591 and 10.5281/zenodo.20696278; code at
  github.com/magickme/soyga) found f = V − 1 in the Section 18 verse, read code words from the
  name triads (13 to 19 of 23 clean, depending on the reading), and noted the Moon repair
  xvi → vi.
- **Ilir Ivezaj** (2026; Zenodo 10.5281/zenodo.20225605) read the code words as drawn from the
  three names, identified MOYSES as the practitioner's table, and gave the Sloane 8 table 1
  erratum (q read as g).
- **Onur Teker** (17 October 2026; Zenodo 10.5281/zenodo.23431833, with a pre-registration at
  10.5281/zenodo.23414455) brought in the Bodley margin note and scored every reading with
  controls: 19 of 23, 131 of 138. Teker named the four misses and noticed the Grisdecon and
  Agatay spellings, after the result and without counting them.
- **Ahmadipour** (github.com/xcodz/decoding-the-book-of-soyga) tested 15 compact families of
  laws for the position numbers on held-out items and found them rejected or weak.
- **orey/book-of-soyga** and **haxlerose/soyga-tables** (GitHub) published implementations of
  Reeds's rule; orey's repository also hosts the Reeds and Kupin PDFs this study reads.

What this study adds, as far as our search found (GitHub, Zenodo and the web, 19 October 2026,
including the previous 60 days):
1. **The ISIAPO repair**: the Bodley numbers counted on Messias with one s. We found it
   nowhere earlier. From v1.2: the Sloane copy's numbers differ from Bodley's by exactly the
   one-s / two-s count at 4 of 5 changed places (chance about 0.0001), which supports it.
2. **One error model, fixed in advance, that explains all four misses**, with a measured
   chance for each (0.00002 to 0.00044) and no wrong code word produced. The Agatay and
   Grisdecon spellings are Teker's observation and xvi → vi is Louv's; what is new is that one
   declared model admits all four, says how unlikely each is by luck, and admits nothing else.
3. **A test of the error model on the printed copies' own disagreements**, with no code words
   used.
4. **The vowel and three-name tests**, and the failure of five rule families, which together
   favour free choice over a hidden rule for the positions.

## 7. Caveats and open checks

1. **The manuscripts.** Everything here is read from Kupin's edition. The images of Sloane 8
   ff. 138v–141r and Bodley 908 do not appear to be online (Teker says the same). A reading of
   the four paragraphs in the manuscripts could confirm or overturn the repairs: Messias or
   Mesias at Cancer, xvi or vi at Moon, and the spellings of Agathay and Griisdecon in the
   name lists.
2. **The Cancer line is uncertain in the edition** (and the v1.2 comparison uses Teker's reading of the Sloane line). Kupin marks the Latin numbers "[? could be
   xviiii]", and the Latin and the translation disagree. ISIAPO rests on the Bodley numbers
   printed in braces.
3. **The error model was written after reading the earlier work.** Two of the four repairs
   (Agatay, Grisdecon) were already noticed by Teker and one (xvi → vi) by Louv. The model is
   generic (any numeral, any attested spelling, any one-letter count slip, in any paragraph),
   and its chance figures measure how much freedom it has; but it was not blind to those
   three.
4. **"Chosen, not generated"** is the reading the evidence weighs toward, not a proof. A rule
   outside the families tested could still exist.
5. **Our transcription.** `data/section28.json` was typed from the edition by hand. Its
   numbers reproduce Teker's independent scores (19 of 23, 131 of 138), which is a check on
   both.

## 8. How to reproduce

Needs Linux or macOS with `python3` (standard library only), `git`, `curl`, `unzip` and
`pdftotext` (poppler).

```
scripts/fetch_sources.sh sources/downloads    # about 25 MB; checks SHA-256 sums
code/run_all.sh sources/downloads             # about a minute and a half on one CPU
git status --short results/ data/             # should be empty
```

`fetch_sources.sh` pins the orey repository to the commit used and checks each download
against `sources/SHA256SUMS`, the copies the published results were made from (downloaded
19 October 2026). If a source has changed since, the script warns and the results may differ.
From these copies the pipeline rebuilds every results file byte for byte (checked from a clean
fetch on 19 October 2026).

The two manuscript excerpts are rebuilt into `data/manuscript_excerpts.json`, which git
ignores, so a rebuild never republishes them by accident.

## Licensing

- **Code** (`code/`, `scripts/`): MIT, see `LICENSE`.
- **Our data and results** (`data/`, `results/`): CC BY 4.0
  (https://creativecommons.org/licenses/by/4.0/). `data/section28.json` is our own
  transcription of the numbers and names of a sixteenth-century text as printed in Kupin's
  edition, with a few words quoted where the edition is unsure; `data/name_variants.json` is
  counts of spellings, rebuilt by `code/name_variants.py`.

**Left out, and why:**
- **Kupin's edition** (PDF and text): copyright; used for research, not redistributed.
  Fetched from the orey repository.
- **Reeds's 1998 preprint**: no licence stated; fetched, not included.
- **The printed manuscript cells** (Kupin's six rows of table 1 and Reeds's 13 rows of
  table 5): tables from those two works, so they are rebuilt locally from the fetched PDFs and
  not published. The results keep only the counts and the handful of cells that disagree.
- **orey's and Louv's generated tables**: fetched for the comparison; only the counts of equal
  cells are published.
- **Teker's preprint, supplement and code** (CC BY 4.0): they could be shared, but the pipeline
  does not need them; fetched for comparison.
- **Ahmadipour's archive**: all rights reserved; read only, not used by the code.
- No manuscript images are included.

## References

- British Library, Sloane MS 8; Bodleian Library, MS Bodley 908.
- Jim Reeds, "John Dee and the Magic Tables in the Book of Soyga" (preprint, 1998); in
  Stephen Clucas (ed.), *John Dee: Interdisciplinary Studies in English Renaissance Thought*
  (Springer, 2006).
- Jane Kupin, *The Book of Soyga* (2014), transcription and translation.
- Jason Louv (2026), Zenodo 10.5281/zenodo.20635591 and 10.5281/zenodo.20696278;
  https://github.com/magickme/soyga
- Ilir Ivezaj (2026), Zenodo 10.5281/zenodo.20225605.
- Onur Teker, "How the Book of Soyga Builds Its Tables and Reads Names from Them" (preprint,
  code and data, 17 October 2026), Zenodo 10.5281/zenodo.23431833; pre-registration
  10.5281/zenodo.23414455.
- Ahmadipour, https://github.com/xcodz/decoding-the-book-of-soyga
- https://github.com/orey/book-of-soyga; https://github.com/haxlerose/soyga-tables

## How to cite

Burford, B. (2026). The Book of Soyga: how the 23 Section 28 code words were chosen. Zenodo. https://doi.org/10.5281/zenodo.23470965 (this DOI always points to the latest version; each release has its own version DOI on Zenodo).
