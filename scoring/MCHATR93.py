import re
from Data import Data

# MCHATR93 — چک‌لیست اصلاح‌شدهٔ غربالگری اوتیسم در نوپایی، تجدیدنظرشده (M-CHAT-R)، ۲۰ گویه، گزارش والد.
# مرجع: M-CHAT-R_impl_scoring_norms_fa.md (بستهٔ MCHATR-FA-AK2014-D1).
#
# هر گویه دو گزینه دارد: 1 = «بله»، 2 = «خیر». کلید (نمرهٔ ۱ برای پاسخ در جهت خطر):
#   گویه‌های ۱، ۳، ۴، ۶..۱۱، ۱۳..۲۰: «خیر» = 1؛ گویه‌های ۲، ۵، ۱۲ (معکوس): «بله» = 1.
# total = جمع ۲۰ گویه (۰..۲۰، عدد صحیح).
# risk: ۰..۲ -> low؛ ۳..۷ -> moderate؛ ۸..۲۰ -> high. هنجار و برش دیگری ندارد.
# rescreen: فقط اگر risk = low و سن کودک < ۲۴ ماه، 1؛ در غیر این صورت 0 (هم‌شکل ستون جدول نتایج).
#
# همه‌یا‌هیچ: گویهٔ بی‌پاسخ -> incomplete؛ سن کودک ثبت‌نشده، غیرعددی، غیرصحیح یا بیرون از ۱۶..۴۸ ماه،
# یا پاسخ بیرون از دو گزینه -> invalid؛ در هر دو total، risk و rescreen همه None. خانهٔ خالی صفر نیست.

ITEMS = 20
YES, NO = 1, 2
REVERSED = (2, 5, 12)                       # «بله» در جهت خطر
AGE_MIN, AGE_MAX = 16, 48                   # دامنهٔ معتبر سن کودک به ماه
RESCREEN_BELOW = 24                         # پیام غربال مجدد زیر ۲۴ ماه
LEVELS = ((0, 2, 'low'), (3, 7, 'moderate'), (8, 20, 'high'))

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')
_WHOLE = re.compile(r'[0-9]+(?:\.0+)?')


def option(answer):
    """شمارهٔ گزینه 1 یا 2؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
    if answer is None:
        return MISSING
    if isinstance(answer, (bool, float)):
        return INVALID
    text = str(answer).translate(_DIGITS).strip()
    if text == '':
        return MISSING
    if text not in ('1', '2'):
        return INVALID
    return int(text)


def months(answer):
    """سن کودک به ماه، عدد صحیح؛ هر مقدار دیگر (خالی، غیرعددی، کسری) نامعتبر."""
    if answer is None or isinstance(answer, bool):
        return INVALID
    if isinstance(answer, int):
        return answer
    if isinstance(answer, float):
        return int(answer) if answer.is_integer() else INVALID
    text = str(answer).translate(_DIGITS).strip()
    if not _WHOLE.fullmatch(text):
        return INVALID
    return int(text.split('.')[0])


def empty():
    return {'total': None, 'risk': None, 'rescreen': None}


def compute(answers, child_age):
    """answers: پاسخ‌های خام ۲۰ گویه به ترتیب فرم؛ child_age: پاسخ خام پیش‌نیاز سن کودک به ماه.
    خروجی: (status, {total, risk, rescreen})."""
    if len(answers) != ITEMS:
        return 'invalid', empty()
    age = months(child_age)
    if age is INVALID or not AGE_MIN <= age <= AGE_MAX:
        return 'invalid', empty()
    raw = [option(a) for a in answers]
    if any(v is INVALID for v in raw):
        return 'invalid', empty()
    if any(v is MISSING for v in raw):
        return 'incomplete', empty()
    total = sum(1 for n, v in enumerate(raw, 1) if v == (YES if n in REVERSED else NO))
    risk = next(name for low, high, name in LEVELS if low <= total <= high)
    rescreen = 1 if (risk == 'low' and age < RESCREEN_BELOW) else 0
    return 'valid', {'total': total, 'risk': risk, 'rescreen': rescreen}


class MCHATR93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        age = self.prerequisite('child_age')
        status, scores = compute(answers, age.get('user_answered') if age else None)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
