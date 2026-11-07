from Data import Data

# STAXI-2 — سیاههٔ بیان خشم حالت–صفت، ویرایش دوم؛ فرم بزرگسال ۵۷ گویه‌ای، فارسی، فرم A.
# مرجع: STAXI-2_impl_scoring_norms_fa.md (بستهٔ STAXI2-FA57-M1)؛ کلید: جدول ۱ و ۲ پایان‌نامهٔ مقدسین (۱۳۸۹).
#
# پنجاه‌وهفت گویه، همه گزینه‌ای و اجباری، در سه بخش (۱ تا ۱۵، ۱۶ تا ۲۵، ۲۶ تا ۵۷)؛
# گزینه 1..4 -> ارزش خام 1..4 (همان شماره). گویهٔ معکوس ندارد.
# دوازده نمره، همه جمع ساده و عدد صحیح، بدون وزن و بدون گردکردن:
#   state_anger        (S-Ang   حالت خشم)                          = ۱ تا ۱۵                       15..60
#   state_feeling      (S-Ang/F احساس خشم)                         = 1، 2، 3، 6، 10                5..20
#   state_verbal       (S-Ang/V احساس تمایل به بیان کلامی خشم)     = 4، 9، 12، 13، 15              5..20
#   state_physical     (S-Ang/P احساس تمایل به بیان جسمی خشم)      = 5، 7، 8، 11، 14               5..20
#   trait_anger        (T-Ang   صفت خشم)                           = ۱۶ تا ۲۵                      10..40
#   trait_temperament  (T-Ang/T خوی خشمناک)                        = 16، 17، 18، 21                4..16
#   trait_reaction     (T-Ang/R واکنش خشمناک)                      = 19، 20، 23، 25                4..16
#   expression_out     (AX-O    بیان خشم به طرف بیرون)             = 27، 31، 35، 39، 43، 47، 51، 55  8..32
#   expression_in      (AX-I    بیان خشم به طرف درون)              = 29، 33، 37، 41، 45، 49، 53، 57  8..32
#   control_out        (AC-O    کنترل خشم به طرف بیرون)            = 26، 30، 34، 38، 42، 46، 50، 54  8..32
#   control_in         (AC-I    کنترل خشم به طرف درون)             = 28، 32، 36، 40، 44، 48، 52، 56  8..32
#   expression_index   (AX      شاخص بیان خشم) = AX-O + AX-I − (AC-O + AC-I) + 48                   0..96
# گویه‌های ۲۲ و ۲۴ فقط در trait_anger هستند. نمرهٔ کل وجود ندارد و ساخته نمی‌شود.
#
# خروجی هر نمره <name>_raw (خام) و <name>_percent است: نمره ÷ بیشینهٔ همان نمره × 100، گردشده به
# عدد صحیح با نیمه به بالا (۳۷٫۵ -> ۳۸)، سپس تقسیم بر ۱۰۰ برای ذخیره در بازهٔ صفر تا یک. گردکردن با
# حساب صحیح است، نه round() که نیمه را به زوج می‌برد. صفرِ expression_index نمرهٔ واقعی است.
# هنجار، صدک، نمرهٔ استاندارد، طبقه، برچسب و هشدار نه محاسبه می‌شود و نه ذخیره.
#
# همه‌یا‌هیچ: یک پاسخ مفقود (incomplete) یا یک مقدار بیرون از 1..4 و شمار گویه جز ۵۷ (invalid)
# هر بیست‌وچهار نمره را None می‌کند؛ پاسخ مفقود با هیچ مقداری پر نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 57
OPTIONS = 4
SCALES = {
    'state_anger': tuple(range(1, 16)),
    'state_feeling': (1, 2, 3, 6, 10),
    'state_verbal': (4, 9, 12, 13, 15),
    'state_physical': (5, 7, 8, 11, 14),
    'trait_anger': tuple(range(16, 26)),
    'trait_temperament': (16, 17, 18, 21),
    'trait_reaction': (19, 20, 23, 25),
    'expression_out': (27, 31, 35, 39, 43, 47, 51, 55),
    'expression_in': (29, 33, 37, 41, 45, 49, 53, 57),
    'control_out': (26, 30, 34, 38, 42, 46, 50, 54),
    'control_in': (28, 32, 36, 40, 44, 48, 52, 56),
}
INDEX_CONSTANT = 48
SCORES = (*SCALES, 'expression_index')
MAXIMUM = {**{name: OPTIONS * len(items) for name, items in SCALES.items()}, 'expression_index': 96}

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def value(answer):
    """گزینه 1..4 -> ارزش خام 1..4 ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
    if answer is None:
        return MISSING
    if isinstance(answer, (bool, float)):
        return INVALID
    text = str(answer).translate(_DIGITS).strip()
    if text == '':
        return MISSING
    if not (text.isascii() and text.isdigit()) or not 1 <= int(text) <= OPTIONS:
        return INVALID
    return int(text)


def percent(score, maximum):
    """درصد صحیحِ گردشده با نیمه به بالا، به صورت نسبت صفر تا یک."""
    return ((200 * score + maximum) // (2 * maximum)) / 100


def compute(answers):
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, {کلید: مقدار})."""
    empty = {name + suffix: None for name in SCORES for suffix in ('_raw', '_percent')}
    if len(answers) != ITEMS:
        return 'invalid', empty
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', empty
    if any(v is MISSING for v in values):
        return 'incomplete', empty
    raw = dict(enumerate(values, 1))
    scores = {name: sum(raw[n] for n in items) for name, items in SCALES.items()}
    scores['expression_index'] = (scores['expression_out'] + scores['expression_in']
                                  - (scores['control_out'] + scores['control_in']) + INDEX_CONSTANT)
    result = {}
    for name in SCORES:
        result[name + '_raw'] = scores[name]
        result[name + '_percent'] = percent(scores[name], MAXIMUM[name])
    return 'valid', result


class STAXI293(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, scores = compute(answers)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
