from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
from Data import Data
from scoring.dictionary.CPRS93 import NORMS_1978, PERSIAN_TABLES

# CPRS93 — فرم کوتاه ویژهٔ والدین مقیاس درجه‌بندی کانرز (CPRS-48)، ۴۸ گویه، گزارش والد.
# مرجع: CPRS_impl_scoring_norms_fa.md (بستهٔ CPRS48-FA-SH2007-D1).
#
# هر گویه چهار گزینه دارد؛ گزینهٔ 1..4 -> ارزش خام 0..3. گویهٔ معکوس ندارد.
# دو نمره‌گذاری از یک پاسخ‌نامه:
#   بلوک ۱، عوامل کلاسیک ۱۹۷۸ (classic_*): نمره میانگین گویه‌ها؛
#     T = 50 + 10 × (میانگین − M) ÷ SD با M و SD جنسیت و گروه سنی کودک (۶..۸ یا ۹..۱۱)،
#     میانگین گردنشده در فرمول، T گرد به نزدیک‌ترین عدد صحیح و نیمه رو به بالا، بی‌سقف (۳۳..۱۷۵)؛
#     میانگین برای نمایش دو رقم اعشار، نیمه رو به بالا. رتبهٔ درصدی ندارد.
#   بلوک ۲، عوامل منبع فارسی (persian_*): نمره جمع گویه‌ها؛ T و رتبهٔ درصدی از جدول، بی‌تفکیک سن و جنسیت.
#     گویه‌های ۱۱ و ۱۳ در conduct و psychosomatic هر دو؛ total جمع هر ۴۸ گویه است، نه جمع عامل‌ها.
#     رتبهٔ درصدی متن است: عدد، یا با «<» همان‌طور که در جدول آمده.
#
# همه‌یا‌هیچ: پاسخ مفقود -> incomplete؛ مقدار نامعتبر، یا جنسیت یا سن کودک ثبت‌نشده یا بیرون از گزینه‌ها
# -> invalid؛ در هر دو، همهٔ نمره‌های هر دو بلوک None. خانهٔ خالی صفر نیست.

ITEMS = 48
CLASSIC = {
    'conduct': (2, 8, 14, 19, 20, 27, 35, 39),
    'learning': (10, 25, 31, 37),
    'psychosomatic': (32, 41, 43, 44),
    'impulsive_hyperactive': (4, 5, 11, 13),
    'anxiety': (12, 16),
    'hyperkinesis_index': (4, 7, 11, 13, 14, 25, 31, 33, 37, 38),
}
PERSIAN = {
    'conduct': (2, 11, 13, 14, 15, 19, 20, 23, 25, 27, 28, 29, 34, 35, 36, 46),
    'social': (3, 10, 17, 18, 30, 31, 37, 38, 39, 47),
    'psychosomatic': (9, 11, 13, 24, 40, 41, 42, 43, 44, 48),
    'anxiety_shyness': (7, 8, 16, 21, 26, 33),
}
CHILD_GENDER = {1: 'F', 2: 'M'}           # دختر، پسر
CHILD_AGE = {1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 11}

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def option(answer, count):
    """شمارهٔ گزینه 1..count ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
    if answer is None:
        return MISSING
    if isinstance(answer, (bool, float)):
        return INVALID
    text = str(answer).translate(_DIGITS).strip()
    if text == '':
        return MISSING
    if not (text.isascii() and text.isdigit()) or not 1 <= int(text) <= count:
        return INVALID
    return int(text)


def half_up(value, places):
    """گرد کردن یک Fraction، نیمه رو به بالا."""
    exact = Decimal(value.numerator) / Decimal(value.denominator)
    return exact.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def empty():
    keys = [f'classic_{name}_{part}' for name in CLASSIC for part in ('mean', 't')]
    keys += [f'persian_{name}_{part}' for name in list(PERSIAN) + ['total'] for part in ('raw', 't', 'pr')]
    return {key: None for key in keys}


def compute(answers, child_gender, child_age):
    """answers: پاسخ‌های خام ۴۸ گویه به ترتیب فرم؛ child_gender و child_age: پاسخ خام دو پیش‌نیاز.
    خروجی: (status, {نام: مقدار})."""
    if len(answers) != ITEMS:
        return 'invalid', empty()
    gender = option(child_gender, len(CHILD_GENDER))
    age = option(child_age, len(CHILD_AGE))
    if gender in (MISSING, INVALID) or age in (MISSING, INVALID):
        return 'invalid', empty()
    raw = [option(a, 4) for a in answers]
    if any(v is INVALID for v in raw):
        return 'invalid', empty()
    if any(v is MISSING for v in raw):
        return 'incomplete', empty()
    item = {n: v - 1 for n, v in enumerate(raw, 1)}
    group = '6-8' if CHILD_AGE[age] <= 8 else '9-11'
    norms = NORMS_1978[(CHILD_GENDER[gender], group)]
    result = {}
    for name, numbers in CLASSIC.items():
        mean = Fraction(sum(item[n] for n in numbers), len(numbers))
        m, sd = (Fraction(Decimal(x)) for x in norms[name])
        result[f'classic_{name}_mean'] = float(half_up(mean, 2))
        result[f'classic_{name}_t'] = int(half_up(50 + 10 * (mean - m) / sd, 0))
    sums = {name: sum(item[n] for n in numbers) for name, numbers in PERSIAN.items()}
    sums['total'] = sum(item.values())
    for name, value in sums.items():
        t, pr = PERSIAN_TABLES[name][value]
        result[f'persian_{name}_raw'] = value
        result[f'persian_{name}_t'] = t
        result[f'persian_{name}_pr'] = pr
    return 'valid', result


class CPRS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        gender = self.prerequisite('child_gender')
        age = self.prerequisite('child_age')
        status, scores = compute(answers,
                                 gender.get('user_answered') if gender else None,
                                 age.get('user_answered') if age else None)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
