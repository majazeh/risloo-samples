from Data import Data

# RSSS — مقیاس کشمکش‌های مذهبی و معنوی، فرم A (فرم فارسی ۲۶ گویه‌ای، ابراهیمی جمارانی و همکاران ۱۴۰۱).
# مرجع: RSSS_impl_scoring_norms_fa.md (بسته RSSS-FA26-J1).
#
# بیست‌وشش گویه، همه گزینه‌ای و اجباری، یک مجموعه گزینه؛ گزینه 1..5 -> ارزش 1..5 (همان شماره).
# هیچ گویه‌ای معکوس نیست و هیچ وزنی در کار نیست. هفت نمره، همه میانگین ساده (1.00..5.00):
#   divine           (DIV) = گویه‌های 1..5
#   demonic          (DEM) = گویه‌های 6..9
#   interpersonal    (INT) = گویه‌های 10..14
#   moral            (MOR) = گویه‌های 15..18
#   ultimate_meaning (MEA) = گویه‌های 19..22
#   doubt            (DOU) = گویه‌های 23..26
#   total            (TOT) = هر ۲۶ گویه — میانگین ۲۶ گویه، نه میانگین شش نمره
#
# محاسبه بر جمع دقیق گویه‌هاست و گردکردن فقط آخرین گام است: دو رقم اعشار، نیمه به بالا، با حساب
# صحیح (نه round() که نیمه را به زوج می‌برد، و نه بریدن). شش مولفه همیشه دقیق‌اند (گام 0.2 یا
# 0.25)؛ فقط total گرد می‌شود. مقدار گردشده همان عددی است که نمایش داده می‌شود و هیچ محاسبه‌ای
# از آن ساخته نمی‌شود. جمع خام، درصد، صدک، نمرهٔ استاندارد، طبقه، برچسب و «حوزهٔ غالب» نه محاسبه
# می‌شود و نه ذخیره.
#
# همه‌یا‌هیچ: یک پاسخ مفقود (incomplete) یا یک مقدار بیرون از 1..5 و شمار گویه جز ۲۶ (invalid)
# هر هفت نمره را None می‌کند؛ پاسخ مفقود با 1 یا هر مقدار دیگری پر نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 26
OPTIONS = 5
SCALES = {
    'divine': (1, 2, 3, 4, 5),
    'demonic': (6, 7, 8, 9),
    'interpersonal': (10, 11, 12, 13, 14),
    'moral': (15, 16, 17, 18),
    'ultimate_meaning': (19, 20, 21, 22),
    'doubt': (23, 24, 25, 26),
    'total': tuple(range(1, ITEMS + 1)),
}

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def value(answer):
    """گزینه 1..5 -> ارزش 1..5 ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
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


def mean(total, count):
    """میانگین دقیق total/count، گردشده به دو رقم اعشار، نیمه به بالا."""
    return (2 * total * 100 + count) // (2 * count) / 100


def compute(answers):
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, {نمره: مقدار})."""
    empty = {name: None for name in SCALES}
    if len(answers) != ITEMS:
        return 'invalid', empty
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', empty
    if any(v is MISSING for v in values):
        return 'incomplete', empty
    return 'valid', {name: mean(sum(values[n - 1] for n in items), len(items))
                     for name, items in SCALES.items()}


class RSSS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, scores = compute(answers)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
