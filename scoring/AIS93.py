from Data import Data

# AIS — مقیاس بی‌خوابی آتن، فرم A (AIS-8 فارسی، نامزد ترکیبی).
# مرجع: AIS_impl_scoring_norms_fa.md (بسته AIS-FA8-C2).
#
# هشت گویه، همه گزینه‌ای و اجباری؛ گزینه 1..4 -> ارزش 0..3. هیچ گویه‌ای معکوس نیست و هیچ وزنی
# در کار نیست؛ هفت مجموعه گزینه فقط در متن فرق دارند، نه در ارزش.
#
# کل = جمع ساده هر هشت گویه (0..24). تنها نمره همین است: خرده‌مقیاس «شبانه» یا «روزانه»،
# طبقه، برچسب و مقایسه با برش مرجع (6) نه محاسبه می‌شود و نه ذخیره — برش فقط متن نیم‌رخ است.
#
# نمایش همه‌یا‌هیچ: پاسخ مفقود (incomplete) یا مقدار بیرون از گزینه‌ها و شمار گویه جز هشت (invalid)
# هیچ نمره‌ای نمی‌گیرد؛ مقدار اصلاح، بریده یا جانشین نمی‌شود و «بی‌نمره» صفر نیست.

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


class AIS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, total = compute(answers)
        score.set('status', status)
        score.set('total', total)
