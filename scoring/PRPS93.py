from Data import Data

# PRPS — مقیاس حل مساله دینی، فرم A (فرم فارسی ۳۶ گویه‌ای، ترجمهٔ نیما قربانی).
# مرجع: PRPS_impl_scoring_norms_fa.md (بسته PRPS-FA36-C1).
#
# سی‌وشش گویه، همه گزینه‌ای و اجباری، یک مجموعه گزینه؛ گزینه 1..5 -> ارزش 1..5 (همان شماره).
# هیچ گویه‌ای معکوس نیست — گویه‌های خودجهت‌دهی هم معکوس نمی‌شوند — و هیچ وزنی در کار نیست.
# سه نمرهٔ جدا، جمع ساده؛ نمرهٔ کل، تفاضل سبک‌ها، میانگین گویه، صدک و «سبک غالب» تعریف
# نشده‌اند و ساخته نمی‌شوند:
#   collaborative  (COL) = گویه‌های 1, 5, 6, 10, 13, 18, 19, 23, 25, 30, 31, 36  (12..60)
#   self_directing (SDR) = گویه‌های 3, 7, 8, 12, 14, 17, 20, 24, 26, 27, 29, 35  (12..60)
#   deferring      (DEF) = گویه‌های 2, 4, 9, 11, 15, 16, 21, 22, 28, 32, 33, 34  (12..60)
# درصد هر مؤلفه از بیشینهٔ ۶۰: نیمه به بالا به درصد صحیح، سپس تقسیم بر ۱۰۰؛
# خروجی و ذخیره‌سازی با پسوند _percent در بازهٔ 0..1؛ اکسل همین مقدار را می‌گیرد.
#
# همه‌یا‌هیچ: یک پاسخ مفقود (incomplete) یا یک مقدار بیرون از 1..5 و شمار گویه جز ۳۶ (invalid)
# هر سه نمره و درصدشان را None می‌کند؛ پاسخ اصلاح، بریده، گرد یا جانشین نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 36
OPTIONS = 5
SCALES = {
    'collaborative': (1, 5, 6, 10, 13, 18, 19, 23, 25, 30, 31, 36),
    'self_directing': (3, 7, 8, 12, 14, 17, 20, 24, 26, 27, 29, 35),
    'deferring': (2, 4, 9, 11, 15, 16, 21, 22, 28, 32, 33, 34),
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


def compute(answers):
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, {نمره: مقدار})."""
    empty = {key: None for name in SCALES for key in (name, name + '_percent')}
    if len(answers) != ITEMS:
        return 'invalid', empty
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', empty
    if any(v is MISSING for v in values):
        return 'incomplete', empty
    scores = {}
    for name, items in SCALES.items():
        raw = sum(values[n - 1] for n in items)
        scores[name] = raw
        scores[name + '_percent'] = ((200 * raw + 60) // 120) / 100
    return 'valid', scores


class PRPS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, scores = compute(answers)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
