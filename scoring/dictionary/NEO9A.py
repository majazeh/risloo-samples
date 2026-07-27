# NEO9A - self-contained dictionary (60-item NEO-FFI short form, 5 domains, no facets).
# Originally a verbatim port of App\ScoreNEO9A (PHP); the norm table has since been
# reconciled with attachment 5 (see the notes on the norm dict below).

domains = ['n', 'e', 'o', 'a', 'c']
facets = []                       # the short form has no facets

# Max raw score per domain: 12 items x 4 = 48
DOMAIN_MAX = 48
maxes = {d: DOMAIN_MAX for d in domains}

# Item (1..60) -> domain. 5-long cycle: i -> ['n','e','o','a','c'][(i-1) % 5]
factors = {i: domains[(i - 1) % 5] for i in range(1, 61)}

# 27 reverse-scored items (attachment 4). Identical to the NEO9V set.
reverse = {
    1, 3, 8, 9, 12, 14, 15, 16, 18, 23, 24, 27, 29, 30, 31, 33, 38, 39,
    42, 44, 45, 46, 48, 54, 55, 57, 59,
}

# Per-option counts are stored for every form, but this one defines no random-responding
# rule: NEO9A/inter.md has no random-responding / acquiescence / nay-saying clause and
# the spec file only asks for the validity column. So no run threshold is declared and
# the per-option run flags always stay 1. (An earlier revision carried thresholds copied
# from the 240-item form; they had no basis for a 60-item form and were removed.)
VOPTION_THRESHOLDS = {}

# Self-report validity items and their error rule - form Neo60 (Garousi Farshi).
# Test fixtures must be generated from this very form; building a fixture from a
# different form was the root cause of a real bug in this family.
FORM = 'Neo60'
# Row discriminator in the shared score_neos table. Item count alone is NOT enough:
# NEO93/NEO9Q both have 240 items and NEO9A/NEO9V both have 60, so the Garousi and
# Haghshenas variants would collide. The 'h' prefix marks the Haghshenas forms.
TYPE = '60'
N_ITEMS = 60
VALIDITY_ITEMS = (61, 62, 63)
# Item 61: plain ascending Likert -> disagreement {1,2} is the error.
# Items 62/63: two-option yes=1 / no=2 -> only "no" = {2} is the error.
VE_ERROR = {61: {1, 2}, 62: {2}, 63: {2}}

# Non-gendered raw-score bands -> level 1..5, taken straight from attachment 5.
# Each list holds the upper bound of five bands: very low, low, average, high, very high.
# Two corrections against the legacy ScoreNEO9A::$norm port, both of which disagreed
# with attachment 5:
#   o : th[0] 24 -> 23. Attachment 5 puts the "low" band at 24-27, so a raw 24 must
#       not fall into "very low".
#   a : th[1] and th[2] were swapped ([27,33,31,...]), which made level 3 unreachable.
#       Column A in attachment 5 is perfectly monotonic: 0-27 / 28-31 / 32-33 / 34-37 / 38-48.
# Note: _level never reads the fifth element; it is kept only for shape consistency.
norm = {
    "n": [15, 20, 25, 31, 48],
    "e": [22, 26, 29, 32, 48],
    "o": [23, 27, 29, 32, 48],
    "a": [27, 31, 33, 37, 48],
    "c": [27, 32, 35, 39, 48],
}
