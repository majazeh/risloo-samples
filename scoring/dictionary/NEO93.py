# NEO93 - self-contained dictionary (item->scale map, reverse items, gendered raw-score bands).
# Source: NEO93/inter.md plus attachments 3..7 (Sina documents - Dr Garousi Farshi).
# Map and reverse set were reconciled with attachments 3/4; the norm tables were
# extracted straight from attachments 5 and 6.

domains = ['n', 'e', 'o', 'a', 'c']

# 30 facets grouped by domain: n1..n6, e1..e6, ... c1..c6
facets = ['{}{}'.format(d, i) for d in domains for i in range(1, 7)]

# Max raw score: domain = 48 items x 4 = 192, facet = 8 items x 4 = 32
DOMAIN_MAX = 192
FACET_MAX = 32
maxes = {k: (DOMAIN_MAX if len(k) == 1 else FACET_MAX) for k in domains + facets}

# Item (1..240) -> facet. 30-long cycle: i -> ORDER[(i-1) % 30]
# ORDER = n1,e1,o1,a1,c1, n2,e2,o2,a2,c2, ... n6,e6,o6,a6,c6  (== attachment 3)
_ORDER = ['{}{}'.format(d, i) for i in range(1, 7) for d in domains]
factors = {i: _ORDER[(i - 1) % 30] for i in range(1, 241)}

# 106 reverse-scored items (attachment 4). Identical to the NEO9Q set - both are
# 240-item long forms.
reverse = {
    1, 4, 7, 8, 10, 11, 14, 17, 18, 20, 21, 24, 27, 28, 30, 32, 33, 35, 36, 39,
    42, 43, 45, 46, 49, 52, 53, 55, 56, 59, 61, 64, 67, 68, 70, 71, 74, 77, 78, 80,
    81, 84, 87, 88, 90, 92, 93, 95, 96, 99, 102, 103, 105, 106, 109, 112, 113, 115, 116, 119,
    121, 124, 127, 128, 130, 134, 137, 138, 140, 141, 144, 147, 148, 150, 153, 155, 156, 159, 162, 163,
    166, 169, 173, 175, 176, 181, 183, 187, 189, 190, 198, 199, 205, 206, 207, 208, 213, 219, 220, 222,
    228, 229, 231, 234, 236, 238,
}

# --- validity thresholds (inter.md) ---
# Random responding: length of a consecutive run of one option that reaches the
# threshold "or more". Keys are option numbers in Neo240.json for items 1..240,
# which are laid out in ascending order:
#   1=strongly disagree -> 6, 2=disagree -> 9, 3=neutral -> 10,
#   4=agree -> 14, 5=strongly agree -> 9
# The previous value {1:9,2:14,3:10,4:9,5:6} was a legacy port of app/ScoreNEO.php,
# which assumed the old descending option layout. Against the current form and
# inter.md that mapping is mirrored, i.e. wrong.
VOPTION_THRESHOLDS = {1: 6, 2: 9, 3: 10, 4: 14, 5: 9}

ACQUIESCENCE_MIN = 150   # (agree + strongly agree) >= 150 -> caution: acquiescence
# Comparison includes 50 ("less than or equal to 50"), matching NEO9Q per the
# scientific team's ruling.
NAY_SAYING_MAX = 50      # (agree + strongly agree) <= 50 -> caution: nay-saying

AGE_MIN = 17             # suitable for 17 and older; below that raises an alert only

# Self-report validity items and their error rule - form Neo240 (Garousi Farshi).
# Test fixtures must be generated from this very form; building a fixture from a
# different form was the root cause of a real bug in this family.
FORM = 'Neo240'
# Row discriminator in the shared score_neos table. Item count alone is NOT enough:
# NEO93/NEO9Q both have 240 items and NEO9A/NEO9V both have 60, so the Garousi and
# Haghshenas variants would collide. The 'h' prefix marks the Haghshenas forms.
TYPE = '240'
N_ITEMS = 240
VALIDITY_ITEMS = (241, 242, 243)
# Item 241: options are laid out in REVERSE on this form
#           (strongly agree=1 ... strongly disagree=5) -> disagreement = {4,5} is the error.
# Items 242/243: two-option yes=1 / no=2 -> only "no" = {2} is the error.
VE_ERROR = {241: {4, 5}, 242: {2}, 243: {2}}

# --- raw-score bands -> level 1..5 (attachment 5 men / attachment 6 women) ---
# Each list holds the upper bound of five bands: very low, low, average, high, very high.
# Level: raw<=th[0]->1, <=th[1]->2, <=th[2]->3, <=th[3]->4, else 5.
# th[4] is never read; it is kept only to stay faithful to the source table.
# One table is picked per respondent: woman(1)->woman, men(2)->men.
# The "total" table (attachment 7) was dropped by the scientific team, so gender is
# mandatory and scoring raises without it.
# Note: across all 35 scales the level-determining thresholds are identical in the
# men and women tables; they differ only at th[4], which never affects a level.
norm = {
    'men': {
        "n": [72, 86, 98, 112, 169], "e": [89, 100, 109, 120, 168], "o": [96, 104, 112, 121, 161],
        "a": [107, 116, 126, 136, 169], "c": [102, 115, 126, 138, 181],
        "n1": [10, 14, 17, 20, 32], "n2": [9, 12, 14, 17, 31], "n3": [13, 16, 19, 22, 32],
        "n4": [14, 16, 19, 22, 31], "n5": [9, 12, 15, 18, 30], "n6": [8, 11, 14, 17, 28],
        "e1": [16, 19, 21, 24, 32], "e2": [12, 15, 18, 21, 32], "e3": [10, 13, 15, 18, 32],
        "e4": [13, 15, 17, 20, 32], "e5": [14, 15, 18, 20, 32], "e6": [14, 17, 19, 23, 32],
        "o1": [11, 14, 17, 20, 30], "o2": [18, 21, 23, 26, 32], "o3": [14, 17, 19, 21, 32],
        "o4": [11, 13, 15, 17, 30], "o5": [16, 18, 21, 24, 32], "o6": [13, 15, 17, 19, 30],
        "a1": [15, 18, 21, 24, 32], "a2": [17, 20, 23, 26, 32], "a3": [18, 21, 23, 25, 32],
        "a4": [13, 15, 18, 21, 29], "a5": [14, 17, 19, 22, 31], "a6": [18, 20, 22, 24, 32],
        "c1": [16, 18, 20, 23, 32], "c2": [15, 18, 20, 22, 32], "c3": [19, 21, 24, 26, 32],
        "c4": [16, 19, 21, 24, 32], "c5": [14, 17, 19, 22, 30], "c6": [15, 18, 20, 23, 32],
    },
    'woman': {
        "n": [72, 86, 98, 112, 169], "e": [89, 100, 109, 120, 159], "o": [96, 104, 112, 121, 171],
        "a": [107, 116, 126, 136, 169], "c": [102, 115, 126, 138, 181],
        "n1": [10, 14, 17, 20, 32], "n2": [9, 12, 14, 17, 31], "n3": [13, 16, 19, 22, 31],
        "n4": [14, 16, 19, 22, 31], "n5": [9, 12, 15, 18, 31], "n6": [8, 11, 14, 17, 32],
        "e1": [16, 19, 21, 24, 32], "e2": [12, 15, 18, 21, 31], "e3": [10, 13, 15, 18, 32],
        "e4": [13, 15, 17, 20, 32], "e5": [14, 15, 18, 20, 32], "e6": [14, 17, 19, 23, 32],
        "o1": [11, 14, 17, 20, 32], "o2": [18, 21, 23, 26, 32], "o3": [14, 17, 19, 21, 32],
        "o4": [11, 13, 15, 17, 26], "o5": [16, 18, 21, 24, 32], "o6": [13, 15, 17, 19, 30],
        "a1": [15, 18, 21, 24, 32], "a2": [17, 20, 23, 26, 32], "a3": [18, 21, 23, 25, 32],
        "a4": [13, 15, 18, 21, 29], "a5": [14, 17, 19, 22, 31], "a6": [18, 20, 22, 24, 32],
        "c1": [16, 18, 20, 23, 31], "c2": [15, 18, 20, 22, 32], "c3": [19, 21, 24, 26, 32],
        "c4": [16, 19, 21, 24, 32], "c5": [14, 17, 19, 22, 31], "c6": [15, 18, 20, 23, 32],
    },
}
