from Data import Data

# ISI — شاخص شدت بی‌خوابی مورین، فرم A (نسخه فارسی صادقی‌نیت، هم‌خوان با ISI-P).
# مرجع: ISI_impl_scoring_norms_fa.md (بسته ISI-FA-ISIP-D1).
#
# هفت گویه، همه گزینه‌ای و اجباری؛ گزینه 1..5 -> ارزش 0..4. هیچ گویه‌ای معکوس نیست —
# گویه 4 (رضایت) هم نه: لنگرهایش از «خیلی راضی» شروع می‌شوند و 0 همان سر مطلوب است.
#
# F1 شدت نشانه‌های شبانه = گویه 1..4 (0..16) ، F2 اثرهای روزانه = گویه 5..7 (0..12) ، کل = F1 + F2 (0..28)
#
# نمایش همه‌یا‌هیچ: پاسخ مفقود (incomplete) یا مقدار بیرون از گزینه‌ها و شمار گویه جز هفت (invalid)
# هیچ نمره‌ای نمی‌گیرد؛ مقدار اصلاح، بریده یا جانشین نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 7
NOCTURNAL = range(0, 4)
DAYTIME = range(4, 7)

# طبقه شدت فقط روی نمره کل؛ کلید، نه متن. مرزها: 0-7 ، 8-14 ، 15-21 ، 22-28.
SEVERITY = [(7, 'none'), (14, 'subthreshold'), (21, 'moderate'), (28, 'severe')]

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def value(answer):
    """گزینه 1..5 -> ارزش 0..4 ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
    if answer is None:
        return MISSING
    if isinstance(answer, (bool, float)):
        return INVALID
    text = str(answer).translate(_DIGITS).strip()
    if text == '':
        return MISSING
    if not (text.isascii() and text.isdigit()) or not 1 <= int(text) <= 5:
        return INVALID
    return int(text) - 1


def severity(total):
    for upper, key in SEVERITY:
        if total <= upper:
            return key


def compute(answers):
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, nocturnal, daytime, total)."""
    if len(answers) != ITEMS:
        return 'invalid', None, None, None
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', None, None, None
    if any(v is MISSING for v in values):
        return 'incomplete', None, None, None
    nocturnal = sum(values[i] for i in NOCTURNAL)
    daytime = sum(values[i] for i in DAYTIME)
    return 'valid', nocturnal, daytime, nocturnal + daytime


class ISI93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, nocturnal, daytime, total = compute(answers)
        score.set('status', status)
        score.set('nocturnal', nocturnal)
        score.set('daytime', daytime)
        score.set('total', total)
        # طبقه توصیف شدت است، نه تشخیص؛ متن و چهار قیدش در نیم‌رخ می‌آیند.
        score.set('severity', None if total is None else severity(total))
