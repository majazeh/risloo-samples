from Data import Data

# CAARS — مقیاس درجه‌بندی ADHD بزرگسالان کانرز، نسخهٔ غربالگری خودگزارشی، فرم A.
# مرجع: CAARS_impl_scoring_norms_fa.md (بسته CAARS-FA30-C1).
#
# سی گویه، همه گزینه‌ای و اجباری؛ گزینه 1..4 -> ارزش 0..3. هیچ گویه‌ای معکوس نیست و هیچ وزنی نیست.
# سه نمرهٔ جدا، جمع ساده؛ نمرهٔ کل و «نشانه‌های کلی» تعریف نشده‌اند و ساخته نمی‌شوند:
#   inattention  (IN)  = گویه‌های 1, 9, 13, 14, 15, 19, 21, 29, 30             (0..27)
#   hyperactivity (HI) = گویه‌های 2, 3, 4, 6, 8, 11, 18, 20, 25 — شامل گویهٔ 3 (0..27)
#   adhd_index   (IDX) = گویه‌های 5, 7, 10, 12, 16, 17, 22, 23, 24, 26, 27, 28 (0..36)
#
# هیچ T، صدک، طبقه یا برچسبی محاسبه نمی‌شود؛ برش مرجع (T ≥ 65 و T ≥ 55) فقط متن نیم‌رخ است و
# هیچ نمره‌ای با آن سنجیده نمی‌شود.
#
# همه‌یا‌هیچ: یک پاسخ مفقود (incomplete) یا یک مقدار بیرون از گزینه‌ها و شمار گویه جز سی (invalid)
# هر سه نمره را None می‌کند؛ مقدار اصلاح، بریده یا جانشین نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 30
OPTIONS = 4
SCALES = {
    'inattention': (1, 9, 13, 14, 15, 19, 21, 29, 30),
    'hyperactivity': (2, 3, 4, 6, 8, 11, 18, 20, 25),
    'adhd_index': (5, 7, 10, 12, 16, 17, 22, 23, 24, 26, 27, 28),
}

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
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, {نمره: مقدار})."""
    empty = {name: None for name in SCALES}
    if len(answers) != ITEMS:
        return 'invalid', empty
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', empty
    if any(v is MISSING for v in values):
        return 'incomplete', empty
    return 'valid', {name: sum(values[n - 1] for n in items) for name, items in SCALES.items()}


class CAARS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, scores = compute(answers)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
