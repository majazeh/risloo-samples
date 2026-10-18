from Data import Data

# OHQ — پرسشنامهٔ شادکامی آکسفورد، فرم A (ترجمهٔ فارسی هادی‌نژاد و زارعی ۱۳۸۸، ۲۹ گویه).
# مرجع: OHQ_impl_scoring_norms_fa.md (بسته OHQ-FA-HZ1388-D1).
#
# بیست‌ونه گویه، همه گزینه‌ای و اجباری، یک مجموعه گزینه؛ گزینه 1..6 -> ارزش خام 1..6 (همان شماره).
# یازده گویهٔ معکوس (1، 6، 10، 13، 14، 19، 23، 24، 27، 28، 29): نمره = 7 − ارزش خام؛ بقیه مستقیم.
# گویهٔ 5 (معکوس در فرم) در هیچ نمره‌ای نیست: پاسخش اجباری است و فقط اعتبارش سنجیده می‌شود.
# هشت نمره، همه جمع ساده و عدد صحیح، بدون وزن:
#   self_concept       (F1 خودپنداره)          = 1، 6، 10، 13، 14، 19، 23، 24   8..48
#   life_satisfaction  (F2 رضایت از زندگی)      = 3، 9، 12                         3..18
#   mental_fitness     (F3 آمادگی روانی)        = 18، 20، 21، 25                   4..24
#   cheerfulness       (F4 سرِ ذوق بودن)        = 11، 15                           2..12
#   aesthetic_sense    (F5 احساس زیبایی‌شناختی) = 2، 4، 7، 16، 27                  5..30
#   self_efficacy      (F6 خودکارآمدی)          = 8، 17، 22، 26                    4..24
#   hope               (F7 امیدواری)            = 28، 29                           2..12
#   total              (T نمرهٔ کل شادکامی)     = جمع هفت عامل، یعنی همهٔ گویه‌ها جز 5   28..168
#
# درصد نمایشی هر نمره، <name>_percent = نمره ÷ بیشینهٔ همان نمره × 100، گردشده به عدد صحیح، نیمه
# به بالا، سپس تقسیم بر ۱۰۰ برای خروجی و ذخیره‌سازی در بازهٔ صفر تا یک.
# گردکردن با حساب صحیح است (نه round() که نیمه را به زوج می‌برد، و نه بریدن). کمینه صفر درصد نیست
# (کمینهٔ هر نمره 17٪ است). صدک، هنجار، برش، طبقه، برچسب و نمرهٔ استاندارد نه محاسبه می‌شود و نه ذخیره.
#
# همه‌یا‌هیچ: یک پاسخ مفقود (incomplete) یا یک مقدار بیرون از 1..6 و شمار گویه جز ۲۹ (invalid)
# هر شانزده نمره را None می‌کند؛ پاسخ مفقود با هیچ مقداری پر نمی‌شود و «بی‌نمره» صفر نیست.

ITEMS = 29
OPTIONS = 6
REVERSED = (1, 6, 10, 13, 14, 19, 23, 24, 27, 28, 29)
FACTORS = {
    'self_concept': (1, 6, 10, 13, 14, 19, 23, 24),
    'life_satisfaction': (3, 9, 12),
    'mental_fitness': (18, 20, 21, 25),
    'cheerfulness': (11, 15),
    'aesthetic_sense': (2, 4, 7, 16, 27),
    'self_efficacy': (8, 17, 22, 26),
    'hope': (28, 29),
}
SCORES = (*FACTORS, 'total')
MAXIMUM = {**{name: OPTIONS * len(items) for name, items in FACTORS.items()},
           'total': OPTIONS * sum(len(items) for items in FACTORS.values())}

MISSING = object()
INVALID = object()

# نرمال‌سازی ارقام فارسی/عربی فقط برای خواندن؛ گزینه و معنا عوض نمی‌شود.
_DIGITS = str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789')


def value(answer):
    """گزینه 1..6 -> ارزش خام 1..6 ؛ خالی مفقود است و هر چیز دیگر نامعتبر."""
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
    """درصد صحیحِ گرد‌شده با نیمه به بالا، به صورت نسبت صفر تا یک."""
    return ((200 * score + maximum) // (2 * maximum)) / 100


def compute(answers):
    """answers: پاسخ‌های خام به ترتیب فرم ؛ خروجی: (status, {نمره: مقدار})."""
    empty = {key: None for name in SCORES for key in (name, name + '_percent')}
    if len(answers) != ITEMS:
        return 'invalid', empty
    values = [value(a) for a in answers]
    if any(v is INVALID for v in values):
        return 'invalid', empty
    if any(v is MISSING for v in values):
        return 'incomplete', empty
    keyed = {n: (OPTIONS + 1 - v if n in REVERSED else v) for n, v in enumerate(values, 1)}
    scores = {name: sum(keyed[n] for n in items) for name, items in FACTORS.items()}
    scores['total'] = sum(scores.values())
    result = {}
    for name in SCORES:
        result[name] = scores[name]
        result[name + '_percent'] = percent(scores[name], MAXIMUM[name])
    return 'valid', result


class OHQ93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        answers = [item.get('user_answered') for item in self.get_items_entirely()]
        status, scores = compute(answers)
        score.set('status', status)
        for name, mark in scores.items():
            score.set(name, mark)
