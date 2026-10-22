from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import re

from Data import Data
from loader import loader
import scoring.dictionary.MCMI93 as d

# MCMI93 — آزمون شخصیت میلون ۳ (MCMI-III)، ۱۷۵ سؤال بلی (۱) / خیر (۲).
#
# انتقال بی‌تغییرِ نمره‌گذاری قبلی risloo (app/ScoreMCMI93.php، VERSION 1.0.2) به
# پایتون؛ دستور پژوهشگر، ۲۰۲۶-۱۰-۲۲. هدف این است که برای هر پاسخ‌نامه همان مقادیری
# در جدول نمره بنشیند که پیش‌تر می‌نشست؛ ترتیب مراحل، گردکردن و مقایسه‌ها همان است:
#
#   ۱. سن: بی سنِ عددی نمره‌گذاری متوقف می‌شود (هیچ نتیجه‌ای ساخته نمی‌شود)؛
#      سن کمتر از ۱۸ نمره می‌گیرد ولی نامعتبر است.
#   ۲. کمتر از ۱۵۷ پاسخ، V خامِ ۲ یا بیشتر، X خامِ بیرون از ۳۴ تا ۱۷۸، و نرسیدنِ
#      هیچ‌یک از 1 تا 8B به BR ۶۰ (پس از همهٔ اصلاح‌ها) نتیجه را نامعتبر می‌کند.
#   ۳. BR از جدول؛ pr همان BR پیش از اصلاح‌هاست؛ سپس اصلاح X، اصلاح 1/2X، اصلاح AD
#      (بستری با روزهای بستری تمام‌رقمی، وگرنه سرپایی)، اصلاح بستری، DC و DD.
#
# ناهمخوانی‌های شناخته‌شده با مستندات دریافتی عمداً بازتولید شده‌اند و پرسش باز
# پژوهشگرند: BR صفر برای خامِ بیرون از جدول (2B، SS و Z در بیشینه)، مرز ۳۴ جدول BR
# افشاگری، max به‌جای min در اصلاح AD سرپایی، روزهای بستری «0» (اصلاح AD بستری بله،
# اصلاح بستری نه)، گرد نشدن X و BRهای اعشاری، و بی‌اثر بودن جنسیت.
#
# خروجی برای هر کد {raw, pr, br} است و risloo آن را به <code>_raw، <code>_pr و
# <code>_br تخت می‌کند؛ به‌علاوهٔ status، messages (همهٔ دلیل‌ها به ترتیب، بی‌تکرار)
# و فقط در حالت نامعتبر message (دلیل اول)، همان‌طور که مدل قبلی می‌نوشت.
#
# معنای مقایسه‌ها و تبدیل‌ها همان PHP 7 است که risloo روی آن اجرا می‌شود (نگاه کنید به
# توابع پایین فایل)؛ round همیشه نیمه را از صفر دور می‌کند.

_WS = ' \t\n\r\v\f'
_NUMERIC = re.compile(r'[' + _WS + r']*[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?', re.ASCII)
_ABSENT = object()


class MCMI93(Data):
    scores = {'raw': None}

    def __init__(self, data, type='raw'):
        # Data سن را با int(float(...)) کوتاه می‌کند و هر رشته‌ای را که پایتون عدد بداند
        # (مثلاً «۳۰» یا «1_8») می‌پذیرد؛ مقدار خام سن پیش از آن جدا نگه داشته می‌شود تا
        # همان آزمون is_numeric در PHP روی آن اجرا شود.
        sheet = loader(data, type).load()
        if type == 'object':
            sheet = deepcopy(sheet)
        self.raw_age = _ABSENT
        for pre in sheet.get('prerequisites') or []:
            if isinstance(pre, dict) and pre.get('label') == 'age':
                self.raw_age = pre.pop('user_answered', None)
        super().__init__(sheet, 'object')

    def scoring_raw(self, score):
        self.messages = []
        prerequisites = getattr(self, '_Data__prerequisites', {})

        age = self.raw_age
        if age is _ABSENT or age is None or not php_is_numeric(age):
            raise ValueError('MCMI93 scoring aborted: client age is required')
        if php_number(age) < d.MIN_AGE:
            self.invalid(d.messages['age'])

        answers = {}
        answered = 0
        for i, item in self.items():
            if 'user_answered' in item:
                answered += 1
                answers[i + 1] = item['user_answered']
        if answered < d.MIN_ANSWERED:
            self.invalid(d.messages['blank'])

        raw = {}
        for code, groups in d.key.items():
            raw[code] = 0
            for weight, value, items in ((2, d.YES, groups[0]), (1, d.YES, groups[1]), (1, d.NO, groups[2])):
                hits = sum(1 for number in set(items) if number in answers and php_equals(answers[number], value))
                raw[code] += hits * weight
        if raw['v'] >= 2:
            self.invalid(d.messages['v'])

        raw['x'] = (raw['1'] + raw['2a'] + raw['2b'] + raw['3'] + raw['4'] + (raw['5'] * 0.67)
                    + raw['6a'] + raw['6b'] + raw['7'] + raw['8a'] + raw['8b'])
        x = raw['x']
        if x < d.X_VALID_MIN or x > d.X_VALID_MAX:
            self.invalid(d.messages['x'])

        br = {'v': raw['v']}
        for code, table in d.br_table.items():
            br[code] = table[raw[code]] if 0 <= raw[code] < len(table) else 0
        br['x'] = x_base_rate(x)
        pr = {code: br[code] for code in d.codes}

        # اصلاح X و 1/2X
        shift = edit(d.x_edit, x)
        for code in d.x_edit_scales:
            br[code] += shift
        shift = edit(d.x12_edit, x)
        for code in d.x12_edit_scales:
            br[code] += shift

        # اصلاح AD
        ad = 0
        if br['d'] >= d.AD_CUT and br['a'] < d.AD_CUT:
            ad = br['d'] - d.AD_CUT
        elif br['d'] >= d.AD_CUT and br['a'] >= d.AD_CUT:
            ad = (br['a'] - d.AD_CUT) + (br['d'] - d.AD_CUT)
        if 'hospitalized' not in prerequisites:
            raise ValueError('MCMI93 scoring aborted: the hospitalized prerequisite is not defined')
        days = prerequisites['hospitalized'].get('user_answered')
        if php_ctype_digit(days) and ad:
            if php_less(days, 7):
                for code in d.ad_scales_1:
                    br[code] -= php_round(min(ad, 25))
                for code in d.ad_scales_2:
                    br[code] -= php_round(min(ad, 20))
            elif php_less_equal(days, 28):
                for code in d.ad_scales_1:
                    br[code] -= php_round(min(ad / 2, 15))
                for code in d.ad_scales_2:
                    br[code] -= php_round(min(0.75 * ad, 15))
        elif ad:
            for code in d.ad_scales_1:
                br[code] -= max(0.25 * ad, 15)
            for code in d.ad_scales_2:
                br[code] -= max(0.125 * ad, 10)

        # اصلاح بستری
        if php_truthy(days):
            if php_less(days, 7):
                br['cc'] += 10
                br['pp'] += 4
                br['ss'] += 8
            elif php_less_equal(days, 28):
                br['cc'] += 7
                br['pp'] += 2
                br['ss'] += 5

        # DC: بیشینهٔ یکتای 4، 5 و 7 هشت واحد می‌گیرد
        top = '4'
        for code in d.dc_scales:
            if br[code] > br[top]:
                top = code
        b4, b5, b7 = br['4'], br['5'], br['7']
        if not ((b4 == b5 and b5 == b7) or (b4 == b5 and b5 > b7)
                or (b4 == b7 and b7 > b5) or (b5 == b7 and b7 > b4)):
            br[top] += 8

        # DD
        dd = php_round((br['y'] - br['z']) / 10)
        for code in d.dd_scales:
            br[code] += min(max(-10, dd), 10)

        if not any(br[code] >= d.BR_CUT for code in d.personality):
            self.invalid(d.messages['br'])

        for code in d.codes:
            score.set(code, {'raw': raw[code], 'pr': pr[code], 'br': br[code]})
        score.set('status', 'invalid' if self.messages else 'valid')
        if self.messages:
            score.set('message', self.messages[0])
        score.set('messages', list(self.messages))

    def invalid(self, text):
        if text not in self.messages:
            self.messages.append(text)


def x_base_rate(x):
    lower = -1
    for upper, value in zip(d.x_br_upper, d.x_br):
        if lower < x <= upper:
            return value
        lower = upper
    raise ValueError('MCMI93 scoring aborted: X raw score is outside the base-rate table')


def edit(table, x):
    if x <= table[0][0] or x >= table[-1][0]:
        return 0
    for (lower, _), (upper, value) in zip(table, table[1:]):
        if lower < x <= upper:
            return value
    return 0


# ---------------------------------------------------------------- PHP 7 semantics

def php_round(value):
    """round() with halves away from zero; PHP returns a float."""
    return float(Decimal(value).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def php_is_numeric(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if not isinstance(value, str):
        return False
    match = _NUMERIC.match(value)
    return bool(match) and match.end() == len(value)


def php_number(value):
    """A string converted to a number as PHP 7 does in comparisons: its leading numeric part, else 0."""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return value
    if value is None:
        return 0
    match = _NUMERIC.match(str(value))
    if not match:
        return 0
    text = match.group(0).lstrip(_WS)
    if re.search(r'[.eE]', text):
        return float(text)
    number = int(text)
    return number if -2 ** 63 <= number < 2 ** 63 else float(text)


def php_equals(value, number):
    """value == number for an integer option, PHP 7 loose comparison."""
    if value is None:
        return False
    return php_number(value) == number


def php_less(value, number):
    if value is None:
        return bool(number)
    return php_number(value) < number


def php_less_equal(value, number):
    if value is None:
        return True
    return php_number(value) <= number


def php_truthy(value):
    if isinstance(value, str):
        return value not in ('', '0')
    return bool(value)


def php_ctype_digit(value):
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, int):
        if -128 <= value <= 255:
            return 48 <= value % 256 <= 57
        value = str(value)
    if not isinstance(value, str):
        return False
    return value != '' and all('0' <= c <= '9' for c in value)
