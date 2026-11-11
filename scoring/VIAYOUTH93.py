from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
from Data import Data

# VIAYOUTH93 — قوت‌های منش نوجوانان (VIA Youth-96)، فرم ۹۶ گویه‌ای، فارسی، خودگزارشی، ۱۰ تا ۱۷ سال.
# مرجع: VIA-Youth-96_impl_scoring_norms_fa.md (بستهٔ via-youth-fa-r4).
#
# نود و شش گویه، همه گزینه‌ای و اجباری، پنج گزینه؛ پاسخ = جایگاه گزینه p از 1 تا 5.
#   گویهٔ مستقیم (O1، ۹۱ گویه):          نمره = 6 − p
#   گویهٔ معکوس (O2، فقط 5، 7، 17، 30، 42): نمره = p
#   گویهٔ ۴ با وجود نفی در متن مستقیم است. پس از این نگاشت دوباره معکوس نمی‌شود.
# بیست و چهار قوت، هر کدام چهار گویه و هر گویه فقط در یک قوت. نمرهٔ هر قوت:
#   <code>_raw     = میانگین سادهٔ چهار نمره (۱ تا ۵، گام ۰٫۲۵)؛ جمع ۴..۲۰ ذخیره نمی‌شود.
#   <code>_percent = round_half_up(raw ÷ 5، سه رقم اعشار)؛ کسری ۰٫۲۰۰ تا ۱٫۰۰۰، نه صدک و نه هنجار.
# حساب با Fraction و Decimal است، نه ممیز شناور. نمرهٔ کل، نمرهٔ فضیلت، طبقه و برچسب ساخته نمی‌شود.
#
# همه‌یا‌هیچ: شمار گویه جز ۹۶، پاسخ مفقود یا پاسخی جز یکی از 1..5 -> status=invalid و هر ۴۸ نمره
# و age_alert همه None. خانهٔ خالی صفر نیست و با میانگین پر نمی‌شود.
# سن پاسخ‌نامه را نامعتبر نمی‌کند (تصمیم پژوهشگر، 2026-11-11): با ۹۶ پاسخ معتبر همیشه نمره‌گذاری می‌شود و
#   age_alert = 1 اگر سن خالی، مفقود، غیرعددی یا بیرون از 10..17 (هر دو حد شامل) باشد، وگرنه 0.
#   age_alert نمره نیست؛ فقط نمایش آلرت عدم اعتبار را تعیین می‌کند. سامانه سن اعشاری را پیش از
#   فرمول به سال تمام می‌کاهد؛ این شکاف ثبت‌شده است و اینجا جبران نمی‌شود.
# جنسیت، تحصیلات و تأهل در نمره دخالتی ندارند.

ITEMS = 96
OPTIONS = 5
REVERSE = frozenset({5, 7, 17, 30, 42})
AGE_MIN, AGE_MAX = 10, 17

# کد قوت -> چهار گویه؛ ترتیب همان ترتیب جدول نمره‌ها در بسته است.
STRENGTHS = {
    'love': (1, 43, 68, 93),
    'zest': (2, 9, 25, 79),
    'fair': (3, 41, 87, 94),
    'humi': (4, 31, 48, 75),
    'hone': (5, 38, 67, 71),
    'lead': (6, 55, 62, 91),
    'forg': (7, 45, 49, 65),
    'kind': (8, 33, 56, 78),
    'beau': (10, 69, 70, 82),
    'hope': (11, 15, 23, 90),
    'curi': (12, 52, 64, 83),
    'lear': (13, 14, 32, 46),
    'soci': (16, 29, 72, 96),
    'grat': (17, 66, 76, 88),
    'brav': (18, 50, 53, 80),
    'crea': (19, 34, 59, 73),
    'spir': (20, 28, 51, 84),
    'judg': (21, 27, 37, 74),
    'team': (22, 36, 54, 92),
    'prud': (24, 42, 85, 89),
    'self': (26, 30, 44, 77),
    'pers': (35, 39, 58, 61),
    'humo': (40, 57, 60, 86),
    'wisd': (47, 63, 81, 95),
}
MAXIMUM = 5

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def whole(answer):
    """عدد صحیح نامنفیِ نوشته‌شده با رقم؛ خالی مفقود است و هر چیز دیگر (اعشاری، متن، چندگزینه) نامعتبر."""
    if answer is None:
        return MISSING
    if isinstance(answer, (bool, float)):
        return INVALID
    text = str(answer).translate(_DIGITS).strip()
    if text == '':
        return MISSING
    if not (text.isascii() and text.isdigit()):
        return INVALID
    return int(text)


def option(answer):
    """جایگاه گزینه 1..5 ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
    p = whole(answer)
    if p is MISSING or p is INVALID:
        return p
    return p if 1 <= p <= OPTIONS else INVALID


def half_up(value, places):
    """گرد کردن یک Fraction، نیمه رو به بالا."""
    exact = Decimal(value.numerator) / Decimal(value.denominator)
    return exact.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def empty():
    return {'age_alert': None, **{f'{code}_{part}': None for code in STRENGTHS for part in ('raw', 'percent')}}


def age_alert(age):
    """1 اگر سن خالی، غیرعددی یا بیرون از 10..17 باشد؛ وگرنه 0."""
    years = whole(age)
    if years is MISSING or years is INVALID:
        return 1
    return 0 if AGE_MIN <= years <= AGE_MAX else 1


def compute(answers, age):
    """answers: پاسخ‌های خام ۹۶ گویه به ترتیب فرم؛ age: پاسخ خام پیش‌نیاز سن.
    خروجی: (status, {کلید: مقدار})."""
    if len(answers) != ITEMS:
        return 'invalid', empty()
    positions = [option(a) for a in answers]
    if any(p is MISSING or p is INVALID for p in positions):
        return 'invalid', empty()
    item = {n: (p if n in REVERSE else OPTIONS + 1 - p) for n, p in enumerate(positions, 1)}
    result = {'age_alert': age_alert(age)}
    for code, numbers in STRENGTHS.items():
        mean = Fraction(sum(item[n] for n in numbers), len(numbers))
        result[f'{code}_raw'] = float(mean)                        # گام ۰٫۲۵؛ در ممیز شناور دقیق است
        result[f'{code}_percent'] = float(half_up(mean / MAXIMUM, 3))
    return 'valid', result


class VIAYOUTH93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        try:
            age = self.prerequisite('age')
        except AttributeError:                                   # پاسخ‌نامه بدون پیش‌نیاز
            age = None
        status, scores = compute(answers, age.get('user_answered') if age else None)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
