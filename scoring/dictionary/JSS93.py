# -*- coding: utf-8 -*-
# JSS — پرسشنامه رضایت شغلی اسپکتور (Spector's Job Satisfaction Survey)
# 36 items, 5-point Likert (1 = کاملاً مخالفم … 5 = کاملاً موافقم), 9 factors of 4 items.
# Source: temp/JSS/JSS_impl_scoring_norms_fa.md §§1-4 and JSS_impl_items_admin_fa.md §5.

f1 = "pay"                   # A — رضایت از پرداخت‌ها
f2 = "operating_procedures"  # B — فرآیندهای اجرایی کار (شرایط کار)
f3 = "coworkers"             # C — همکاران
f4 = "promotion"             # D — ارتقای شغلی
f5 = "supervision"           # E — نظارت
f6 = "fringe_benefits"       # F — مزایای جانبی شغل
f7 = "contingent_rewards"    # G — پاداش‌های احتمالی
f8 = "nature_of_work"        # H — ماهیت شغل
f9 = "communication"         # K — ارتباطات و اطلاع‌رسانی
f10 = "total"                # نمره کل رضایت شغلی

factors_names = (f1, f2, f3, f4, f5, f6, f7, f8, f9, f10)

# Highest option value of the answer scale. Reversal is (options + 1) - answer,
# i.e. the `6 - raw` rule of the scoring document.
options = 5

# Every item feeds its own factor and the total score.
factors = {
    1: (f1, f10),
    2: (f1, f10),
    3: (f1, f10),
    4: (f1, f10),

    5: (f2, f10),
    6: (f2, f10),
    7: (f2, f10),
    8: (f2, f10),

    9: (f3, f10),
    10: (f3, f10),
    11: (f3, f10),
    12: (f3, f10),

    13: (f4, f10),
    14: (f4, f10),
    15: (f4, f10),
    16: (f4, f10),

    17: (f5, f10),
    18: (f5, f10),
    19: (f5, f10),
    20: (f5, f10),

    21: (f6, f10),
    22: (f6, f10),
    23: (f6, f10),
    24: (f6, f10),

    25: (f7, f10),
    26: (f7, f10),
    27: (f7, f10),
    28: (f7, f10),

    29: (f8, f10),
    30: (f8, f10),
    31: (f8, f10),
    32: (f8, f10),

    33: (f9, f10),
    34: (f9, f10),
    35: (f9, f10),
    36: (f9, f10),
}

# 19 reverse items (scoring doc §2). The remaining 17 are scored directly.
reverse_scoring_numbers = (2, 3, 5, 7, 8, 10, 12, 13, 18, 19, 21, 24, 26, 27, 28, 29, 34, 35, 36)

# Maximum raw score per factor: 4 items × 5 for each factor, 36 × 5 for the total.
maxes = {
    factor: options * sum(1 for item_factors in factors.values() if factor in item_factors)
    for factor in factors_names
}
