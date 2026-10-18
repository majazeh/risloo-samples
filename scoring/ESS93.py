from Data import Data

# ESS — مقیاس خواب‌آلودگی اپوورث، فرم A (نسخهٔ ایرانی بزرگسالان، ESS-IR 2013).
# مرجع: ESS_impl_scoring_norms_fa.md (بسته ESS-FA-IR2013-D1).
#
# هشت گویه، همه گزینه‌ای و اجباری، یک مجموعه گزینه (R1)؛ گزینه 1..4 -> ارزش 0..3.
# هیچ گویه‌ای معکوس نیست و هیچ وزنی در کار نیست.
#
# کل = جمع ساده هر هشت گویه (0..24). تنها نمره همین است: دو مؤلفه‌ای که تحلیل عاملی نسخهٔ
# ایرانی نشان داد عمداً نمره نمی‌گیرند؛ زیرمقیاس، طبقه، برچسب، هنجار و برش «۱۰ و بیشتر»
# نه محاسبه می‌شود و نه ذخیره.
# درصد از بیشینه: گردکردن نیمه به بالا به درصد صحیح، سپس تقسیم بر ۱۰۰؛
# مقدار percent در خروجی و ذخیره‌سازی 0..1 است، بدون تبدیل دوباره در اکسل.
#
# نمایش همه‌یا‌هیچ: پاسخ مفقود (incomplete) یا مقدار بیرون از گزینه‌ها و شمار گویه جز هشت (invalid)
# هیچ نمره‌ای نمی‌گیرد؛ مقدار اصلاح، بریده، گرد یا جانشین نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 8
OPTIONS = 4

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def value(answer):
    """گزینه 1..4 -> ارزش 0..3 ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
    if answer is None:
        return MISSING
    if isinstance(answer, (bool, float)):
        return INVALID
    text = str(answer).translate(_DIGITS).strip()
    if text == '':
        return MISSING
    if not (text.isascii() and text.isdigit()) or not 1 <= int(text) <= OPTIONS:
        return INVALID
    return int(text) - 1


def compute(answers):
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, total)."""
    if len(answers) != ITEMS:
        return 'invalid', None
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', None
    if any(v is MISSING for v in values):
        return 'incomplete', None
    return 'valid', sum(values)


class ESS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, total = compute(answers)
        score.set('status', status)
        score.set('total', total)
        score.set('percent', ((200 * total + 24) // 48) / 100 if total is not None else None)
