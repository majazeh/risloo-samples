from Data import Data
from fractions import Fraction
import math
import re

# PSQI — شاخص کیفیت خواب پیتزبورگ، فرم A (فرم فارسی پیوست پایان‌نامه فرهی مقدم 2009، بدون Q10).
# مرجع: PSQI_impl_scoring_norms_fa.md (بسته PSQI-FA-THESIS2009-D1).
#
# ترتیب گویه‌ها در فرم: Q1..Q4 ، Q5a..Q5j ، Q6..Q9  (18 گویه)
# Q1/Q3 ساعت کامل 0..23 بدون دقیقه (P1، بازنگری 2026-09-24) ، Q2 دقیقه ، Q4 ساعت اعشاری ، بقیه گزینه‌ای 1..4 -> کد 0..3
#
# هیچ گویه‌ای معکوس نمی‌شود. مولفه وابسته به پاسخ مفقود یا نامعتبر، ناموجود (None) است؛
# تنها استثنا Q5j است (اصلاح 20 مه 2005): فراوانی یا توضیح مفقود => 0.
# نمایش همه‌یا‌هیچ: اگر حتی یک مولفه ناموجود باشد، status = invalid و هیچ نمره‌ای خروجی نمی‌گیرد.

Q1, Q2, Q3, Q4 = 0, 1, 2, 3
Q5A, Q5J = 4, 13
Q5B_I = range(5, 13)
Q6, Q7, Q8, Q9 = 14, 15, 16, 17

CUTOFF = 6

components = [
    'subjective_quality',   # C1 کیفیت ذهنی خواب
    'latency',              # C2 تأخیر خواب
    'duration',             # C3 مدت خواب
    'efficiency',           # C4 کارایی معمول خواب
    'disturbances',         # C5 اختلال‌های خواب
    'medication',           # C6 مصرف داروی خواب
    'daytime_dysfunction',  # C7 اختلال عملکرد روزانه
]

MISSING = object()
INVALID = object()

# نرمال‌سازی نمایشی اعداد فارسی/عربی؛ گزینه، واحد و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩٫', '01234567890123456789.')
_HOUR = re.compile(r'^\d{1,2}$')
_NUMBER = re.compile(r'^\d+(\.\d+)?$')


def _text(value):
    if value is None:
        return None
    value = str(value).translate(_DIGITS).strip()
    return value if value != '' else None


def category(value):
    """گزینه 1..4 -> کد 0..3 ؛ هر چیز دیگر نامعتبر (P2)."""
    if value is None or isinstance(value, bool):
        return MISSING if value is None else INVALID
    if isinstance(value, float):
        return INVALID
    text = _text(value)
    if text is None:
        return MISSING
    if not text.isdigit() or not 1 <= int(text) <= 4:
        return INVALID
    return int(text) - 1


def number(value):
    """عدد نامنفی و متناهی، به‌صورت کسر دقیق تا مرزها بدون خطای ممیز شناور سنجیده شوند.
    پاسخ بازه‌ای فقط با دو سر مشخص پذیرفته می‌شود (میانگین دو سر)؛ متن آزاد تبدیل نمی‌شود."""
    if isinstance(value, (list, tuple)):
        if len(value) != 2:
            return INVALID
        low, high = number(value[0]), number(value[1])
        if low in (MISSING, INVALID) or high in (MISSING, INVALID) or low > high:
            return INVALID
        return (low + high) / 2
    if isinstance(value, bool):
        return INVALID
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return INVALID
        value = repr(value)
    text = _text(value)
    if text is None:
        return MISSING
    if not _NUMBER.match(text):
        return INVALID
    return Fraction(text)


def clock(value):
    """ساعت کامل 0..23 -> دقیقه از نیمه‌شب (P1). ساعت با دقیقه، کسر و 24 بدقالب‌اند، نه گردشده."""
    if isinstance(value, bool) or isinstance(value, float) and not value.is_integer():
        return INVALID
    if isinstance(value, float):
        value = int(value)
    text = _text(value)
    if text is None:
        return MISSING
    if not _HOUR.match(text) or int(text) > 23:
        return INVALID
    return int(text) * 60


def ok(*values):
    return all(v is not MISSING and v is not INVALID for v in values)


def latency_minutes(x):
    """L(Q2)"""
    if x <= 15:
        return 0
    if x <= 30:
        return 1
    if x <= 60:
        return 2
    return 3


def pair(s):
    """B(s) — بازکد جمع دو پاسخ 0..6"""
    if s == 0:
        return 0
    if s <= 2:
        return 1
    if s <= 4:
        return 2
    return 3


def duration(hours):
    """C3"""
    if hours >= 7:
        return 0
    if hours >= 6:
        return 1
    if hours >= 5:
        return 2
    return 3


def efficiency(percent):
    """C4"""
    if percent >= 85:
        return 0
    if percent >= 75:
        return 1
    if percent >= 65:
        return 2
    return 3


def disturbances(total):
    """C5"""
    if total == 0:
        return 0
    if total <= 9:
        return 1
    if total <= 18:
        return 2
    return 3


def compute(answers, q5j_description=None):
    """answers: فهرست 18 پاسخ خام به ترتیب فرم ؛ خروجی: فهرست هفت مولفه C1..C7 (None = ناموجود)."""
    q2, q4 = number(answers[Q2]), number(answers[Q4])
    bed, rise = clock(answers[Q1]), clock(answers[Q3])
    q5a = category(answers[Q5A])
    q5 = [category(answers[i]) for i in Q5B_I]
    q5j = category(answers[Q5J])
    q6, q7, q8, q9 = (category(answers[i]) for i in (Q6, Q7, Q8, Q9))

    # P2: ساعت خواب واقعی بیش از 24 نامعتبر است.
    if ok(q4) and q4 > 24:
        q4 = INVALID

    c1 = q6 if ok(q6) else None
    c2 = pair(latency_minutes(q2) + q5a) if ok(q2, q5a) else None
    c3 = duration(q4) if ok(q4) else None

    c4 = None
    if ok(q4, bed, rise):
        in_bed = (rise - bed) % (24 * 60)   # فاصله رو به جلو، با عبور از نیمه‌شب
        # ساعت‌های برابر مبهم‌اند؛ خواب بیش از زمان بستر نامعتبر است و به 100٪ بریده نمی‌شود.
        if in_bed != 0 and q4 * 60 <= in_bed:
            c4 = efficiency(100 * q4 * 60 / in_bed)

    # Q5j مؤثر: فراوانی مفقود یا توضیح خالی => 0 ؛ فراوانی نامعتبر => C5 ناموجود.
    description = _text(q5j_description)
    if q5j is MISSING or description is None and q5j is not INVALID:
        q5j_effective = 0
    else:
        q5j_effective = q5j
    c5 = disturbances(sum(q5) + q5j_effective) if ok(*q5, q5j_effective) else None

    c6 = q7 if ok(q7) else None
    c7 = pair(q8 + q9) if ok(q8, q9) else None
    return [c1, c2, c3, c4, c5, c6, c7]


class PSQI93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        items = self.get_items_entirely()
        answers = [item.get('user_answered') for item in items]
        vector = compute(answers, items[Q5J].get('user_description'))

        valid = all(c is not None for c in vector)
        score.set('status', 'valid' if valid else 'invalid')
        for name, value in zip(components, vector):
            score.set(name, value if valid else None)
        total = sum(vector) if valid else None
        score.set('total', total)
        # نشانگر غربال دوتایی روی نمره کل، نه تشخیص و نه درجه‌بندی شدت.
        score.set('screening', None if total is None else ('positive' if total >= CUTOFF else 'negative'))
