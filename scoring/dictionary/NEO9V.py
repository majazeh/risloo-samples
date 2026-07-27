# NEO9V - self-contained dictionary (60-item NEO-FFI short form, Dr Haghshenas).
# Source: NEO9V/inter.md plus attachment 3 (domains/subscales) and attachment 4
# (reverse-scored items).
#
# Difference from NEO9A: both cover the same 60 items and the same reverse set, but
#   - 9A has only the 5 domains and does have a raw-score description table (attachment 5);
#   - 9V adds the 13 NEO-FFI cluster subscales and has no norm table at all,
#     so only a percentage is reported and level is never produced.
#
# WARNING: the short codes n1/n2/e1..c3 mean something different here than in
# NEO93/NEO9Q - n2 is self_reproach here, not angry_hostility; e3 is activity here,
# not assertiveness. When rows share one table, the type column is what disambiguates them.

domains = ['n', 'e', 'o', 'a', 'c']

# 13 subscales grouped by domain (attachment 3)
facets = ['n1', 'n2', 'e1', 'e2', 'e3', 'o1', 'o2', 'o3', 'a1', 'a2', 'c1', 'c2', 'c3']

# English name of each scale - maps to the spec-file column names
titles = {
    'n': 'neuroticism', 'e': 'extraversion', 'o': 'openness_to_experience',
    'a': 'agreeableness', 'c': 'conscientiousness',
    'n1': 'negative_affect', 'n2': 'self_reproach',
    'e1': 'positive_affect', 'e2': 'sociability', 'e3': 'activity',
    'o1': 'aesthetic_interests', 'o2': 'intellectual_interests', 'o3': 'unconventionality',
    'a1': 'nonantagonistic_orientation', 'a2': 'prosocial_orientation',
    'c1': 'orderliness', 'c2': 'goal_striving', 'c3': 'dependability',
}

# Items of each subscale (attachment 3)
facet_items = {
    'n1': [1, 11, 16, 31, 46],
    'n2': [6, 21, 26, 36, 41, 51, 56],
    'e1': [7, 12, 37, 42],
    'e2': [2, 17, 27, 57],
    'e3': [22, 32, 47, 52],
    'o1': [13, 23, 43],
    'o2': [48, 53, 58],
    'o3': [3, 8, 18, 38],
    'a1': [9, 14, 19, 24, 29, 44, 54, 59],
    'a2': [4, 34, 39, 49],
    'c1': [5, 10, 15, 30, 55],
    'c2': [25, 35, 60],
    'c3': [20, 40, 45, 50],
}

# Item (1..60) -> domain. 5-long cycle: i -> ['n','e','o','a','c'][(i-1) % 5]
# (same cycle as NEO9A, although the two read different forms)
factors = {i: domains[(i - 1) % 5] for i in range(1, 61)}

# Item -> subscale. Items 28 and 33 belong to domain o only and to no subscale;
# attachment 3 lists them separately for exactly that reason.
subfactors = {i: f for f, items in facet_items.items() for i in items}

# Max raw score = item count x 4
DOMAIN_MAX = 48                                    # 12 items x 4
maxes = {d: DOMAIN_MAX for d in domains}
maxes.update({f: len(items) * 4 for f, items in facet_items.items()})

# 27 reverse-scored items (attachment 4) - identical to the NEO9A set
reverse = {
    1, 3, 8, 9, 12, 14, 15, 16, 18, 23, 24, 27, 29, 30, 31, 33, 38, 39,
    42, 44, 45, 46, 48, 54, 55, 57, 59,
}

# --- validity thresholds (inter.md) ---
# "If the number of 'no opinion' answers is 10 or more, the test is not valid."
# "no opinion" is option 3 on this form.
NEUTRAL_OPTION = 3
NEUTRAL_MAX = 10             # count[3] >= 10 -> test is invalid

AGE_MIN = 16                 # below 16 raises an alert only (scientific team ruling)

# Per-option counts are stored for every form, but this one's document defines no
# random-responding rule, so no run threshold is declared and the per-option run flags
# always stay 1.
VOPTION_THRESHOLDS = {}

# Self-report validity items and their error rule - form H60 (Haghshenas).
# Reference form: risloo/resources/assessments/scales/forms/NEO/H60.json (version 5).
# Option layout in H60 mirrors H240 exactly:
#   items 1..61 : ascending 5-point Likert, strongly disagree=1 ... strongly agree=5
#                 -> disagreement = {1,2} is the error
#   items 62/63 : two-option yes=1 / no=2 -> only "no" = {2} is the error
# Test fixtures must be generated from this very form; building a fixture from a
# different form was the root cause of a real bug in this family.
FORM = 'H60'
# Row discriminator in the shared score_neos table. Item count alone is NOT enough:
# NEO93/NEO9Q both have 240 items and NEO9A/NEO9V both have 60, so the Garousi and
# Haghshenas variants would collide. The 'h' prefix marks the Haghshenas forms.
TYPE = 'h60'
N_ITEMS = 60
VALIDITY_ITEMS = (61, 62, 63)
VE_ERROR = {61: {1, 2}, 62: {2}, 63: {2}}

# No norm table: attachments 5/6/7 do not exist for this form and the spec file only
# asks for <name>_raw and <name>_percentage, so no descriptive level exists here.
norm = None

# Value stored in {f}_level when there is no level to report. It must not be null: the
# column is `tinyint unsigned NOT NULL DEFAULT 0`, so a null insert is rejected. Real
# levels run 1..5, which leaves 0 free to mean "not applicable" without ambiguity.
NO_LEVEL = 0
