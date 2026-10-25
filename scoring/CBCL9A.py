from Data import Data
from scoring.dictionary.CBCL9A import T_TABLE, PR_TABLE, PR_ABOVE

# CBCL9A — سیاههٔ رفتاری کودکان پیش‌دبستانی آخنباخ (CBCL/1½-5)، فرم والد ویرایش ۲۰۰۰.
# مرجع: CBCL_impl_scoring_norms_fa.md (بستهٔ CBCL-FA-RT2025-D1).
#
# فرم ۱۰۲ پرسش دارد: گویه‌های ۱ تا ۹۹، و سه بخش گویهٔ ۱۰۰ در پرسش‌های ۱۰۰ تا ۱۰۲.
#   گویه‌های ۱ تا ۹۹: سه گزینه؛ گزینهٔ 1..3 -> ارزش خام 0..2.
#   سه بخش گویهٔ ۱۰۰: دو گزینه؛ گزینهٔ 1..2 -> ارزش 1..2؛ «مشکل دیگری ندارد» خالی ذخیره می‌شود -> 0.
#   نمرهٔ گویهٔ ۱۰۰ بیشینهٔ سه بخش است، نه جمعشان.
# پانزده نمره، همه جمع ساده و بدون وزن؛ هر کدام با جدول T_TABLE به T، با PR_TABLE از T به رتبهٔ درصدی
# و با برش به طبقه برمی‌گردد:
#   سندرم‌ها و مقیاس‌های DSM: T < 65 normal، 65..69 borderline، >= 70 clinical
#   internalizing، externalizing، total: T < 60 normal، 60..63 borderline، >= 64 clinical
# رتبهٔ درصدی متن است: عدد، '>97' (T برابر ۷۰ و بالاتر) یا '≤50' (کف سندرم‌ها و DSM)؛ در طبقه اثری ندارد.
# «سایر مشکلات» نمرهٔ جدا ندارد و فقط در total می‌آید.
#
# شرط نمره‌گرفتن: پیش‌نیاز child_age ثبت شده باشد (گزینهٔ 1..5، همه درون ۱۸ تا ۷۱ ماه).
# همه‌یا‌هیچ: سن کودک نامعتبر یا ثبت‌نشده، یا مقدار نامعتبر -> invalid؛ پاسخ مفقود در گویه‌های
# ۱ تا ۹۹ -> incomplete؛ در هر دو، همهٔ نمره‌ها None. خانهٔ خالی گویه‌های ۱ تا ۹۹ صفر نیست.

ITEMS = 99
PARTS = 3
SCALES = {
    'emotionally_reactive': (21, 46, 51, 79, 82, 83, 92, 97, 99),
    'anxious_depressed': (10, 33, 37, 43, 47, 68, 87, 90),
    'somatic_complaints': (1, 7, 12, 19, 24, 39, 45, 52, 78, 86, 93),
    'withdrawn': (2, 4, 23, 62, 67, 70, 71, 98),
    'sleep_problems': (22, 38, 48, 64, 74, 84, 94),
    'attention_problems': (5, 6, 56, 59, 95),
    'aggressive_behaviour': (8, 15, 16, 18, 20, 27, 29, 35, 40, 42, 44, 53, 58, 66, 69, 81, 85, 88, 96),
    'affective_problems': (13, 24, 38, 43, 49, 50, 71, 74, 89, 90),
    'anxiety_problems': (10, 22, 28, 32, 37, 47, 48, 51, 87, 99),
    'pervasive_developmental_problems': (3, 4, 7, 21, 23, 25, 63, 67, 70, 76, 80, 92, 98),
    'adhd': (5, 6, 8, 16, 36, 59),
    'oppositional_defiant_problems': (15, 20, 44, 81, 85, 88),
}
INTERNALIZING = ('emotionally_reactive', 'anxious_depressed', 'somatic_complaints', 'withdrawn')
EXTERNALIZING = ('attention_problems', 'aggressive_behaviour')
COMPOSITES = ('internalizing', 'externalizing', 'total')
ORDER = ('emotionally_reactive', 'anxious_depressed', 'somatic_complaints', 'withdrawn',
         'sleep_problems', 'attention_problems', 'aggressive_behaviour',
         'internalizing', 'externalizing', 'total',
         'affective_problems', 'anxiety_problems', 'pervasive_developmental_problems',
         'adhd', 'oppositional_defiant_problems')
AGE_OPTIONS = 5

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


def percentile(name, t):
    if t >= 70:
        return PR_ABOVE
    return PR_TABLE['composite' if name in COMPOSITES else 'scale'][t]


def category(name, t):
    if name in COMPOSITES:
        return 'normal' if t < 60 else ('borderline' if t <= 63 else 'clinical')
    return 'normal' if t < 65 else ('borderline' if t <= 69 else 'clinical')


def compute(answers, child_age):
    """answers: پاسخ‌های خام ۱۰۲ پرسش به ترتیب فرم؛ child_age: پاسخ خام پیش‌نیاز سن کودک.
    خروجی: (status, {نام_value / نام_t / نام_status: مقدار})."""
    empty = {name + suffix: None for name in ORDER for suffix in ('_value', '_t', '_pr', '_status')}
    if len(answers) != ITEMS + PARTS:
        return 'invalid', empty
    if option(child_age, AGE_OPTIONS) in (MISSING, INVALID):
        return 'invalid', empty
    raw = [option(a, 3) for a in answers[:ITEMS]]
    parts = [option(a, 2) for a in answers[ITEMS:]]
    if any(v is INVALID for v in raw) or any(v is INVALID for v in parts):
        return 'invalid', empty
    if any(v is MISSING for v in raw):
        return 'incomplete', empty
    item = {n: v - 1 for n, v in enumerate(raw, 1)}
    item[100] = max(0 if p is MISSING else p for p in parts)
    sums = {name: sum(item[n] for n in numbers) for name, numbers in SCALES.items()}
    sums['internalizing'] = sum(sums[s] for s in INTERNALIZING)
    sums['externalizing'] = sum(sums[s] for s in EXTERNALIZING)
    sums['total'] = sum(item[n] for n in range(1, 101))
    result = {}
    for name in ORDER:
        t = T_TABLE[name][sums[name]]
        result[name + '_value'] = sums[name]
        result[name + '_t'] = t
        result[name + '_pr'] = percentile(name, t)
        result[name + '_status'] = category(name, t)
    return 'valid', result


class CBCL9A(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        age = self.prerequisite('child_age')
        status, scores = compute(answers, age.get('user_answered') if age else None)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
