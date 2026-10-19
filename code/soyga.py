"""Book of Soyga tables: alphabet, letter values, Reeds's step function and generator.

Our own implementation, written from Reeds (1998) section 4 and the Section 18 verse
of Kupin's edition (2014); no code copied from other projects.

Alphabet: the 23 letters of the tables, a b c d e f g h i k l m n o p q r s t u x y z
(no j, v, w). Letters are numbered 0..22 here; Reeds numbers them 1..23.
"""

ALPHA = "abcdefghiklmnopqrstuxyz"
IDX = {c: i for i, c in enumerate(ALPHA)}

# Reeds (1998) Table II: the step f(W), "places after the letter above".
F_REEDS = dict(
    a=2,
    b=2,
    c=3,
    d=5,
    e=14,
    f=2,
    g=6,
    h=5,
    i=14,
    k=15,
    l=20,
    m=22,
    n=14,
    o=8,
    p=13,
    q=20,
    r=11,
    s=8,
    t=8,
    u=15,
    x=15,
    y=15,
    z=2,
)

# Section 18 verse (Kupin 2014, Latin text, Sloane 8 f. 64v), our parse, line by line:
VERSE = [
    ("Tres numeros z, b, numeros tres continet a, f.", {"z": 3, "b": 3, "a": 3, "f": 3}),
    ("H bis tres numeros numeratos continet in se.", {"h": 6}),
    ("Septem G, numeros per se portat numeratos.", {"g": 7}),
    ("O plenum cum T, comis est, S ter tria portat.", {"o": 9, "t": 9, "s": 9}),
    ("Bis sex, R, numeros, secum deportat habendos.", {"r": 12}),
    ("Bis septem numeros secum P portat habendas,", {"p": 14}),
    ("E cum n tenet I, numeros ter quinque potenter.", {"e": 15, "n": 15, "i": 15}),
    ("V cum K ut x, y, dat bis octo decenter,", {"u": 16, "k": 16, "x": 16, "y": 16}),
    ("L ut Q, numeros ter vii gaudet habere,", {"l": 21, "q": 21}),
    ("Cumque suis pedibus M xxti tria portat.", {"m": 23}),
    ("Terque novem per se C, iam lunatus habebit.", {"c": 27}),
    ("Vigintique novem D dat cum sumitur ampla,", {"d": 29}),
]
V18 = {}
for _line, vals in VERSE:
    V18.update(vals)
assert set(V18) == set(ALPHA)


def make_f(values, offset):
    """Step function from letter values: f(L) = values[L] - offset (mod 23)."""
    return {c: (values[c] - offset) % 23 for c in ALPHA}


def gen_table(code, f=F_REEDS, n=36):
    """Reeds's rule. Left column: code word and its reverse, repeated. Top row:
    X = W + f(W). Interior: X = N + f(W) (N above, W to the left), mod 23."""
    code = code.lower()
    col = (code + code[::-1]) * (n // 12 + 1)
    g = [[""] * n for _ in range(n)]
    for r in range(n):
        g[r][0] = col[r]
    for c in range(1, n):
        w = g[0][c - 1]
        g[0][c] = ALPHA[(IDX[w] + f[w]) % 23]
    for r in range(1, n):
        for c in range(1, n):
            g[r][c] = ALPHA[(IDX[g[r - 1][c]] + f[g[r][c - 1]]) % 23]
    return ["".join(row) for row in g]


# Reeds (1998) Table I: label and code word of the 36 tables (code words as written in
# the tables' left margins).
TABLES = [
    ("Aries", "NISRAM"),
    ("Taurus", "ROELER"),
    ("Gemini", "IOMIOT"),
    ("Cancer", "ISIAPO"),
    ("Leo", "ORRASE"),
    ("Virgo", "OSACUE"),
    ("Libra", "XUAUIR"),
    ("Scorpio", "RAOSAC"),
    ("Sagitarius", "RSADUA"),
    ("Capricornus", "ATROGA"),
    ("Aquarius", "SDUOLO"),
    ("Pisces", "ARICAA"),
    ("Aries", "MARSIN"),
    ("Taurus", "RELEOR"),
    ("Gemini", "TOIMOI"),
    ("Cancer", "OPAISI"),
    ("Leo", "ESARRO"),
    ("Virgo", "EUCASO"),
    ("Libra", "RIUAUX"),
    ("Scorpio", "CASOAR"),
    ("Sagitarius", "AUDASR"),
    ("Capricornus", "AGORTA"),
    ("Aquarius", "OLOUDS"),
    ("Pisces", "AACIRA"),
    ("Saturni", "OSRESO"),
    ("Jovis", "NIEBOA"),
    ("Martis", "OIAIAE"),
    ("Solis", "ITIABA"),
    ("Veneris", "ADAMIS"),
    ("Mercurii", "REUELA"),
    ("Lunae", "UISEUA"),
    ("Ignis", "MERONF"),
    ("Aeris", "ILIOSU"),
    ("Aquae", "OYNIND"),
    ("Terrai", "IASULA"),
    ("Magistri", "MOYSES"),
]


def norm(s):
    """Fold a Latin spelling into the table alphabet (j->i, v->u, w->u; letters only)."""
    s = s.lower().replace("j", "i").replace("v", "u").replace("w", "u")
    return "".join(c for c in s if c in IDX)
