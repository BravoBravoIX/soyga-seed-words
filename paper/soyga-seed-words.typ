// Working paper for the soyga-seed-words repository. Build: paper/build.sh
#set document(title: "The Book of Soyga: how the Section 28 code words were chosen", author: "Brett Burford")
#set page(paper: "a4", margin: (x: 2.3cm, y: 2.4cm), numbering: "1")
#set text(font: ("Libertinus Serif", "New Computer Modern"), size: 10.5pt, lang: "en", region: "au")
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.3em, below: 0.7em)
#show link: set text(fill: rgb("#1a4f8b"))
#set table(stroke: 0.4pt + luma(150), inset: 5pt)
#show table: set text(size: 9.2pt)
#show table: set par(justify: false)

#align(center)[
  #text(size: 16pt, weight: "bold")[The Book of Soyga: how the Section 28 code words were chosen]
  #v(0.5em)
  #text(size: 11pt)[Brett Burford]
  #v(0.2em)
  #text(size: 9pt)[ORCID #link("https://orcid.org/0009-0003-6599-8297")[0009-0003-6599-8297] · Independent researcher, Australia]
  #v(0.2em)
  #text(size: 9pt)[Working paper, version 1.2.1, 19 October 2026 · not peer reviewed]
  #v(0.2em)
  #text(size: 9pt)[Code, data and results: #link("https://github.com/BravoBravoIX/soyga-seed-words")[github.com/BravoBravoIX/soyga-seed-words], #link("https://doi.org/10.5281/zenodo.23470965")[doi:10.5281/zenodo.23470965]]
]

#v(0.8em)
#block(inset: (x: 1.2cm))[
  #text(weight: "bold")[Abstract.] The thirty-six letter tables of the _Book of Soyga_ (_Aldaraia_; British Library, Sloane MS 8; Bodleian Library, MS Bodley 908) were reconstructed by Jim Reeds (1998, 2006). Louv (2026) found Reeds's step function in the book's own Section 18 verse, and Teker (2026) showed that 19 of the 23 code words spelled out in Section 28 follow exactly from position numbers counted in each book's three divine names, leaving four unexplained: ISIAPO, ARICAA, REUELA and UISEUA. The code words themselves have been known since Reeds (1998); what was open is how these four are derived. This paper reproduces those results from an independent transcription of Kupin's edition and tests one error model, declared before scoring, that allows a single Roman-numeral slip, a spelling the book uses elsewhere, or a slip in counting the letters. Under that model all four open code words are produced with one slip each; the chance that one slip turns the same names into a random six-letter word of the right letters is 0.00044, 0.00005, 0.00002 and 0.00004 respectively, and no paragraph produces any of the other 22 code words even with two slips. The same two kinds of slip are seen, far more often than chance, where the printed copies of the numbers disagree with each other. The ISIAPO repair (the Bodley numbers counted on _Mesias_, "Messias" with one _s_) appears to be new, and the two copies of the Cancer numbers support it: where the Sloane copy differs from the Bodley one, four of five numbers are exactly one higher, as a recount on the two-_s_ spelling would make them (chance about 0.0001). No compact rule generates the positions; the words are vowel-rich and draw on all three names, and the evidence weighs toward free choice by the author.
]

= Introduction

The _Book of Soyga_ is an anonymous sixteenth-century Latin book of magic, surviving in two manuscripts, British Library Sloane MS 8 and Bodleian Library MS Bodley 908; John Dee owned a copy. It ends with thirty-six tables of $36 times 36$ letters. Each table grows from a six-letter code word written down its left margin.

Reeds (1998, 2006) showed how the tables are built. The left column is the code word followed by its reverse, repeated down the 36 rows. Every other cell is the letter above it moved on through the 23-letter alphabet by a step $f$ that depends on the letter to its left. Reeds worked $f$ out from the tables themselves, and described the numbers in the book's text that appear to go with the code words as standing "in unknown relation" to them.

Two questions remained: where $f$ comes from, and how the code words were chosen. Louv (2026) answered the first: a Latin verse in Section 18 gives each letter a value $V$, and $f = V - 1 space (mod 23)$. For the second, Section 28 of the book has 23 short paragraphs, one for each of the twelve signs, the seven planets and the four elements. Each gives a list of numbers, mostly six, and each book of the work has three divine names (for example _Agla_, _Primogenitus_, _On_). A note in the Bodley margin says to count those letters in the three names of each book. Ivezaj (2026) and Louv (2026) read the code words this way, and Teker (2026) did it systematically, with controls, across every printed copy of the numbers and every printed spelling of the names: 19 of the 23 code words come out exactly, 131 of 138 letters. Four stayed open.

This paper asks two questions, both made checkable. First, where the printed numbers miss, is there a repair that is plausible as an ordinary copying or counting slip and better than chance? Second, is there a rule that produces the numbers, or the words, without being told the word?

= Earlier work

- *Reeds* (1998 preprint; 2006 chapter) broke the tables: the generation rule, the step function and the list of code words.
- *Kupin* (2014) published the Latin transcription and English translation from which every number and name here is read.
- *Louv* (2026) found $f = V - 1$ in the Section 18 verse, read code words from the name triads (13 to 19 of 23 clean, depending on the reading) and noted the Moon repair _xvi_ → _vi_.
- *Ivezaj* (2026) read the code words as drawn from the three names, identified MOYSES as the practitioner's table and gave the Sloane 8 table 1 erratum (_q_ read as _g_).
- *Teker* (2026, with a pre-registration) brought in the Bodley margin note and scored every reading against controls: 19 of 23 words, 131 of 138 letters. He named the four misses and noticed the spellings _Agatay_ and _Grisdecon_, after the result and without counting them.
- *Ahmadipour* (GitHub) tested fifteen compact families of laws for the position numbers on held-out items and found them rejected or weak.
- The _orey/book-of-soyga_ and _haxlerose/soyga-tables_ repositories published implementations of Reeds's rule.

= Sources and data

All numbers and names were transcribed by hand from Kupin's edition (Section 28: Latin pp. 533–537, translation pp. 538–541; Sloane 8 ff. 138v–141r, with the Bodley 908 variants printed in braces). The transcription (`data/section28.json`) records every printed copy of each paragraph's numbers: the Latin as printed, Kupin's translation where it reads the Latin differently, the Bodley variants, and the Bodley marginal list for Taurus, together with the Roman numerals as printed and the editor's notes of uncertainty. The code words are those of the tables' left margins (Reeds 1998, Table I). Reeds's preprint and Kupin's edition were read from the copies in the _orey/book-of-soyga_ repository; Louv's and orey's generated tables and Teker's preprint were used for comparison only. No manuscript images were used: images of the relevant leaves do not appear to be online (Teker reports the same).

= Method

Every random process uses the seed 20261019. The whole analysis uses the Python standard library and reruns in about a minute and a half on one CPU.

*Reproduction.* Our own generator builds the 36 tables from Reeds's rule and Louv's $f$. We test $f$ against $V$ at all 23 offsets, against 100,000 shuffled value tables, and compare our tables with two independent implementations and with the only manuscript cells in print (Kupin's six rows of Sloane 8 table 1; Reeds's thirteen rows of table 5), using the other 35 tables as controls.

*Code words from the names.* For each paragraph the printed numbers are applied as positions in the three names joined together. We score three readings: the numbers as printed in the Latin; as given in Kupin's translation; and any printed copy with any printed spelling. Two controls: each paragraph scored against the 22 wrong books' names, and 100,000 random pairings of names with paragraphs.

*The error model*, written into the code before any scoring was run. Each step costs one, and at most two are allowed:
- *numeral slip*: one character added, dropped or changed in one Roman numeral (so _xvi_ can become _vi_ or _xvii_); or two numbers run together (as the Latin "_x, v_" that the translation reads as _xv_); or one number dropped from a list longer than six, or added to a list of five;
- *spelling*: one name replaced by a spelling the book itself uses elsewhere, under a declared rule (one inner letter different, occurring at least twice on the Latin pages of the edition);
- *counting slip*: one letter of the joined names skipped or counted twice, so that every position after that point is one too high or too low.
Every printed copy of the numbers and every spelling printed in Section 28 is a starting point at no cost.

*Chance.* For each paragraph we draw 100,000 random six-letter "code words" from random positions of the same three names, so that they use the right letters, and count how many the same number of slips would also produce. A second control asks whether any paragraph's slips produce one of the other 22 real code words.

*Independent test of the error model.* Using only the printed numbers, never the code words, we classify the disagreements between printed copies of the same paragraph's numbers and compare the shares of each kind of slip with random lists changed at the same rate.

*Rules for the positions.* Using the 23 position lists that give the code words exactly, we test vowel content, use of all three names, preference for first occurrences, rising positions, and five compact rule families, each judged against the same rule applied to the wrong book's names.

= Results

== Reeds's rule and Louv's step function

$f = V - 1 space (mod 23)$ holds for all 23 letters at offset 1 and at no other offset; 100,000 shuffled value tables fit at most 11 letters at any offset. Our 36 tables equal Louv's and orey's in all 46,656 cells. The rule fits 206 of 215 legible cells of Sloane 8 table 1 as printed by Kupin (7 of the 9 misses are _q_ read as _g_, as Ivezaj noted) and 466 of 468 cells of Reeds's table 5; no other table reaches more than 104 and 282 cells respectively.

== The 36 code words

Twelve code words are reverses: tables 13–24 repeat the twelve signs, and their code words are those of tables 1–12 written backwards, as the text says. MOYSES heads the last table, the practitioner's own (as Ivezaj noted). The other 23 are spelled out in Section 28 by position numbers in the three divine names (Table 1). In no reading does any of the 100,000 random pairings reach the real score. Teker reports 115, 113 and 131 letters; the small differences in the first two readings come from how lists that are not six numbers long are scored.

#figure(
  table(
    columns: (1.6fr, 1fr, 1fr, 1fr, 1fr),
    align: (left, center, center, center, center),
    table.header([*Reading of the numbers*], [*Letters (of 138)*], [*Exact words (of 23)*], [*Wrong book, mean letters*], [*Random pairings, max*]),
    [as printed in the Latin], [114], [13], [13.3], [55],
    [as given in Kupin's translation], [112], [13], [13.2], [52],
    [any printed copy, any printed spelling], [131], [19], [17.6], [69],
  ),
  caption: [Code words spelled from the three divine names (`results/sec28.json`).],
)

== The four open code words

Under the declared model, each of the four open code words is produced exactly by one slip (Table 2). With no slips, 19 paragraphs give their code word; with at most one, all 23 do. The largest one-slip chance for any of the 23 paragraphs is 0.0027 (Taurus, which needs no slip). No paragraph produces any of the other 22 code words, even with two slips (0 of $22 times 23$ cross-pairings).

#figure(
  table(
    columns: (auto, auto, 1fr, auto, auto),
    align: (left, left, left, left, center),
    table.header([*Table*], [*Code word*], [*What gives it exactly*], [*Slip*], [*Chance*]),
    [Cancer], [ISIAPO], [the Bodley numbers 4, 15, 4, 5, 7, 11, counted on "Messias" with one _s_ (_Mesias Panton Hos_; dropping any one of the first three letters of _Messias_ gives the same)], [counting], [0.00044],
    [Pisces], [ARICAA], [the printed numbers on _Griszon Misericors Agatay_, the book's usual spelling (7 times, against _Agathay_ once); or _Agathay_ with the last number 22 → 23], [spelling (or numeral)], [0.00005],
    [Mercury], [REUELA], [the printed numbers on _Solus Grisdecon Agatabaii_, the book's usual spelling (6 times, against _Griisdecon_ once)], [spelling], [0.00002],
    [Moon], [UISEUA], [the numbers 17, 13, 14, 10, 17, 16 with the last read _vi_ for _xvi_], [numeral], [0.00004],
  ),
  caption: [The four repairs (`results/repair.json`). "Chance" is the share of 100,000 random six-letter words, drawn from the same names, that one slip would also produce.],
)

== Cancer: the two copies differ by the one-s count

This comparison was added after the first version, so it is an observation tested after the fact, not a prediction (`results/cancer_copies.json`). Table 3 sets the Bodley numbers beside the Sloane main text as Teker (2026) reads it. The Bodley numbers give all six letters of ISIAPO on the one-_s_ spelling. Where the Sloane copy differs (five places), four of its numbers are exactly one higher than Bodley's, and each of those gives the right letter on the two-_s_ spelling _Messias_, which is what a recount of those letters on _Messias_ would produce. If a copyist had changed the numbers at random, four or more of five changes would be exactly one higher in 0.000094 of 1,000,000 trials. Both copies begin with 4 for the first I, and position 4 is I only on the one-_s_ spelling, so even the Sloane copy keeps a trace of a one-_s_ count. The third number fits neither spelling; the Sloane line is corrupt there. The evidence weighs toward the Bodley list being the original one-_s_ count and the Sloane numbers a partial recount on _Messias_. Teker reads the Sloane line the same way but does not compare it with the Bodley numbers on the two spellings.

#figure(
  table(
    columns: (2.4fr, 1fr, 1fr, 1fr, 1fr, 1fr, 1fr),
    align: (left, center, center, center, center, center, center),
    table.header([*Letter of ISIAPO*], [I], [S], [I], [A], [P], [O]),
    [Bodley numbers (ISIAPO on _Mesias_)], [4], [15], [4], [5], [7], [11],
    [Sloane main text (Teker's reading)], [4], [16], [2], [6], [8], [12],
    [Sloane read on _Messias_], [s], [*s*], [e], [*a*], [*p*], [*o*],
  ),
  caption: [The Cancer numbers in the two copies. Bold: Sloane numbers one higher than Bodley's that give the right letter on the two-_s_ spelling.],
)

== The printed copies make the same slips

This test uses only the printed numbers. Of the 18 pairs of printed copies that disagree, 5 differ by one Roman-numeral slip (28 %, against 8 % for random lists changed at the same rate) and 3 by a counting slip, a block of positions all one higher or lower (17 %, against 0.2 %). For example, Taurus has Bodley 8, 14, 2, 10, 4, 1 against 9, 15, 2, 11, 4, 1, and Jupiter has Bodley 16, 14, 10, 20, 19, 6 against 17, 15, 11, 21, 20, 6 (`results/witness_diffs.json`). The two kinds of slip that the repairs rely on are therefore the kinds the scribes and the composer can be seen making elsewhere in the same section.

== No rule behind the positions

The code words are rich in vowels: 82 of 138 letters, against 61.5 expected from random positions in the same names ($p approx 0.0004$). Twenty of the 23 draw on all three names, against 15.1 expected ($p approx 0.02$). Compact rules fail: an arithmetic progression of positions fits Saturn only (7, 9, 11, 13, 15, 17); steps taken from the Section 18 letter values, or from the letters' places in the alphabet, fit none; one step shared by all paragraphs, fitted on the other 22, predicts none held out; a fixed-stride reading through the names fits 9 of 23, against 10.4 expected if each letter's position were chosen at random among its occurrences. Two weaker tendencies are not significant: first occurrences are used 42 times against 35.3 expected ($p approx 0.08$), and positions rise in 60 of 115 steps against 54.4 ($p approx 0.08$) (`results/rules.json`).

= Discussion

*What the evidence weighs toward.* The selection of all 36 code words is accounted for: twelve reverses, MOYSES, and 23 words spelled from the three divine names, 19 exactly as printed and 4 after one ordinary slip each. Each of the four repairs beats chance by three orders of magnitude or more, the model that allows them produces no wrong code word, and the same kinds of slip are seen among the printed copies themselves. No rule that predicts the words from the names was found, here or in Ahmadipour's tests. The evidence weighs toward free choice: the author picked a pronounceable six-letter word from the letters of all three names and wrote down where each letter sits.

*What is new*, as far as a search of GitHub, Zenodo and the web on 19 October 2026 found:
+ the ISIAPO repair, the Bodley numbers counted on _Mesias_, and the finding that the Sloane copy's numbers differ from the Bodley ones by exactly that one-_s_ count at four of five changed places;
+ one error model, fixed in advance, that explains all four misses with a measured chance for each and admits no wrong code word (the _Agatay_ and _Grisdecon_ spellings are Teker's observations and _xvi_ → _vi_ is Louv's; what is new is that one declared model admits all four, measures how unlikely each is by luck, and admits nothing else);
+ a test of the error model on the printed copies' own disagreements, with no code words used;
+ the vowel and three-name tests and the failure of five rule families, which together favour free choice over a hidden rule for the positions.

*Limits.*
+ Everything is read from Kupin's edition. A reading of the four paragraphs in the manuscripts could confirm or overturn the repairs: _Messias_ or _Mesias_ at Cancer, _xvi_ or _vi_ at Moon, and the spellings of _Agathay_ and _Griisdecon_ in the name lists.
+ The Cancer line is uncertain in the edition. Kupin marks the Latin numbers "[? could be xviiii]", and the Latin and the translation disagree; ISIAPO rests on the Bodley numbers printed in braces, and the comparison of the two copies uses Teker's reading of the Sloane line.
+ The error model was written after reading the earlier work, and three of the four repairs had already been noticed (two by Teker, one by Louv). The model is generic (any numeral, any attested spelling, any one-letter counting slip, in any paragraph), and its chance figures measure how much freedom it has; but it was not blind to those three.
+ "Chosen, not generated" is where the evidence weighs, not a proof. A rule outside the families tested could still exist.
+ Our transcription was typed by hand. Its numbers reproduce Teker's independent scores (19 of 23 words, 131 of 138 letters), which is a check on both.

= Data and code availability

Code (MIT), our transcription and all results (CC BY 4.0) are at #link("https://github.com/BravoBravoIX/soyga-seed-words")[github.com/BravoBravoIX/soyga-seed-words] and archived at #link("https://doi.org/10.5281/zenodo.23470965")[doi:10.5281/zenodo.23470965]. Third-party texts are not redistributed; a script fetches them from where their owners publish them and checks their SHA-256 sums, and the pipeline then rebuilds every results file byte for byte.

= Acknowledgements

This study stands on the work of Jim Reeds, Jane Kupin, Jason Louv, Ilir Ivezaj and Onur Teker. The analysis code was written with the help of an AI coding assistant (Claude, Anthropic); the author checked the results and is responsible for any errors.

= References

#set par(hanging-indent: 1.2em, justify: false)
#set text(size: 9.5pt)

Ahmadipour. _Decoding the Book of Soyga_. #link("https://github.com/xcodz/decoding-the-book-of-soyga")[github.com/xcodz/decoding-the-book-of-soyga].

British Library, Sloane MS 8; Bodleian Library, MS Bodley 908.

haxlerose. _soyga-tables_. #link("https://github.com/haxlerose/soyga-tables")[github.com/haxlerose/soyga-tables].

Ivezaj, I. (2026). Zenodo. #link("https://doi.org/10.5281/zenodo.20225605")[doi:10.5281/zenodo.20225605].

Kupin, J. (2014). _The Book of Soyga_: transcription and translation. #link("https://archive.org/details/the-book-of-soyga-jane-kupin")[archive.org/details/the-book-of-soyga-jane-kupin].

Louv, J. (2026). The source of Reeds's function: how the Book of Soyga generates its own tables. Zenodo. #link("https://doi.org/10.5281/zenodo.20635591")[doi:10.5281/zenodo.20635591]\; reproduction package #link("https://doi.org/10.5281/zenodo.20696278")[doi:10.5281/zenodo.20696278]\; #link("https://github.com/magickme/soyga")[github.com/magickme/soyga].

orey. _book-of-soyga_. #link("https://github.com/orey/book-of-soyga")[github.com/orey/book-of-soyga].

Reeds, J. (1998). John Dee and the magic tables in the Book of Soyga. Preprint. #link("https://archive.org/details/jimreedssoyga")[archive.org/details/jimreedssoyga].

Reeds, J. (2006). John Dee and the magic tables in the Book of Soyga. In S. Clucas (ed.), _John Dee: Interdisciplinary Studies in English Renaissance Thought_. Dordrecht: Springer, pp. 177–204. #link("https://doi.org/10.1007/1-4020-4246-9_10")[doi:10.1007/1-4020-4246-9_10].

Teker, O. (2026). How the Book of Soyga builds its tables and reads names from them. Preprint, code and data. Zenodo. #link("https://doi.org/10.5281/zenodo.23431833")[doi:10.5281/zenodo.23431833]\; pre-registration #link("https://doi.org/10.5281/zenodo.23414455")[doi:10.5281/zenodo.23414455].
