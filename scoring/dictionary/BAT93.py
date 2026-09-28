# -*- coding: utf-8 -*-
# BAT — ابزار ارزیابی فرسودگی شغلی (Burnout Assessment Tool), work-related BAT-23.
# 33 items, 5-point frequency scale (1 = هرگز … 5 = همیشه), no reverse items.
# Source: temp/BAT93/BAT_impl_items_admin_fa.md §§3-5 and
#         temp/BAT93/BAT_impl_scoring_norms_fa.md §§1-4.

f1 = "total_core"  # علائم اصلی (نمره کل) — items 1..23
f2 = "ex"          # خستگی — Exhaustion
f3 = "md"          # فاصله ذهنی — Mental distance
f4 = "ci"          # آسیب‌دیدگی شناختی — Cognitive impairment
f5 = "ei"          # آسیب‌دیدگی هیجانی — Emotional impairment
f6 = "secondary"   # علائم ثانویه (نمره کل) — items 24..33
f7 = "pd"          # شکایات روان‌شناختی — Psychological complaints
f8 = "psc"         # شکایات روان‌تنی — Psychosomatic complaints

# Report order, which is also the row order of the profile design.
factors_names = (f1, f2, f3, f4, f5, f6, f7, f8)

# Highest option value of the answer scale.
options = 5

# No item is reverse scored — every item points the same way (higher = more burnout).
reverse_scoring_numbers = ()

# Each item feeds its own subscale and the total of its symptom group. The four
# core subscales roll up into total_core; the two secondary ones into secondary.
factors = {}
for _item in range(1, 9):
    factors[_item] = (f2, f1)
for _item in range(9, 14):
    factors[_item] = (f3, f1)
for _item in range(14, 19):
    factors[_item] = (f4, f1)
for _item in range(19, 24):
    factors[_item] = (f5, f1)
for _item in range(24, 29):
    factors[_item] = (f7, f6)
for _item in range(29, 34):
    factors[_item] = (f8, f6)

# Item count per factor — the divisor of the mean and, times `options`, the raw maximum.
counts = {
    factor: sum(1 for item_factors in factors.values() if factor in item_factors)
    for factor in factors_names
}

# Raw maximum per factor: total_core 115, ex 40, secondary 50, the rest 25.
maxes = {factor: options * counts[factor] for factor in factors_names}

# Flemish clinical cut-offs for BAT-23 (scoring doc §4), applied to the mean score:
# level 1 = سبز «بدون خطر فرسودگی», 2 = نارنجی «در معرض خطر», 3 = قرمز «خطر بسیار بالا».
# The pair is (upper bound of green, upper bound of orange); anything above is red.
# pd and psc are absent on purpose: the manual publishes no cut-off for the two
# secondary subscales on their own, so they report level 0 = «بدون طبقه» and the
# profile prints a dash for them.
LEVEL_NONE = 0
cutoffs = {
    f1: (2.58, 3.01),
    f2: (3.05, 3.30),
    f3: (2.49, 3.09),
    f4: (2.69, 3.09),
    f5: (2.09, 2.89),
    f6: (2.84, 3.34),
}
