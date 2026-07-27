from Data import Data
import scoring.dictionary.MCMI9A as d


class MCMI9A(Data):
    # ترتیب اجرا معنادار است: تعدیل A/CC از BRِ تعدیل‌شده با X خوانده می‌شود و
    # high_point از BRِ نهایی. (روی گزارش‌های واقعی Pearson راستی‌آزمایی شده.)
    scores = {'raw': None, 'br': None, 'correction_x': None, 'correction_acc': None,
              'reports': None, 'levels': None, 'high_point': None}

    # نمره خام همه مقیاس‌ها، ابعاد گراسمن، شاخص‌های V و W و شاخص‌های هشداردهنده
    def scoring_raw(self, score):
        try:
            age = int(self.prerequisite('age', 'user_answered'))
        except (TypeError, ValueError):
            raise ValueError("MCMI9A age notfound")
        if age < d.MIN_AGE:
            raise ValueError("MCMI9A age invalid")

        raw = dict.fromkeys(d.scales + ['x', 'y', 'z'], 0)
        facet = dict.fromkeys(d.facets, 0)
        answers = {}

        for i, item in self.items():
            index = i + 1
            if index > d.N_ITEMS:
                continue
            answer = self._answer(item)
            if answer is None:
                continue
            answers[index] = answer
            if answer == d.TRUE:
                items, facet_items = d.item_true, d.facet_true
            else:
                items, facet_items = d.item_false, d.facet_false
            for code, weight in items.get(index, ()):
                raw[code] += weight
            for code in facet_items.get(index, ()):
                facet[code] += 1

        for code in d.scales:
            score.set(code, {'raw': raw[code], 'br': None, 'level': None})
        for code in d.facets:
            score.set(code, {'raw': facet[code], 'br': None, 'level': None})
        for code in ('x', 'y', 'z'):
            score.set(code, {'raw': raw[code], 'br': None, 'report': None, 'level': None})

        score.set('v', {'raw': sum(answers.get(q) == d.TRUE for q in d.v_items),
                        'report': None})
        score.set('w', {'raw': self._inconsistency(answers), 'report': None})
        score.set('noteworthy', {code: self._noteworthy(answers, code)
                                 for code in d.noteworthy})

    # تبدیل نمره خام به نمره خط پایه (BR)
    def scoring_br(self, score):
        for code in d.scales:
            self._set_br(score, code, d.br[code])
        for code in d.facets:
            self._set_br(score, code, d.facet_br[code])
        for code, table in (('x', d.br_x), ('y', d.br_y), ('z', d.br_z)):
            self._set_br(score, code, table)

    # تعدیل بر اساس نمره خام شاخص افشا (X) — روی هر ۲۵ مقیاس اعمال می‌شود
    def scoring_correction_x(self, score):
        first, second = self._lookup(d.correction_x, score.get('x')['raw'])
        self._shift(score, d.x_group_1, first)
        self._shift(score, d.x_group_2, second)
        score.set('correction', {'x_1': first, 'x_2': second, 'acc_value': 0,
                                 'acc_1': 0, 'acc_2': 0, 'alert': None})

    # تعدیل اضطراب/افسردگی — تنها وقتی که BR مقیاس A یا CC به ۷۵ رسیده باشد
    def scoring_correction_acc(self, score):
        br_a, br_cc = score.get('a')['br'], score.get('cc')['br']
        # دروازه بر پایه «رسیدن به ۷۵» است نه «گذشتن از ۷۵»: اگر هر دو زیر ۷۵
        # باشند هیچ تعدیلی انجام نمی‌شود، ولی BRِ برابر ۷۵ دروازه را باز می‌کند و
        # ارزش صفرِ حاصل در ردیف ۰-۴ جدول پیوست ۷ می‌افتد.
        gate = br_a >= d.ACC_CUT or br_cc >= d.ACC_CUT
        value = max(0, br_a - d.ACC_CUT) + max(0, br_cc - d.ACC_CUT)

        correction = score.get('correction')
        correction['acc_value'] = value
        if gate:
            first, second = d.correction_acc[value]
            self._shift(score, d.acc_group_1, first)
            self._shift(score, d.acc_group_2, second)
            correction['acc_1'], correction['acc_2'] = first, second

        applied = [name for name, on in (('x', correction['x_1'] or correction['x_2']),
                                         ('acc', gate)) if on]
        correction['alert'] = '_'.join(applied) if applied else 'none'

    # تفسیر شاخص‌های اصلاح و اعتبار، و آلرت اعتبار آزمون
    def scoring_reports(self, score):
        for code, bands in (('x', d.x_report), ('y', d.y_report), ('z', d.z_report)):
            obj = score.get(code)
            obj['report'] = self._level(bands, obj['br'])
        for code, bands in (('v', d.v_report), ('w', d.w_report)):
            obj = score.get(code)
            obj['report'] = self._level(bands, obj['raw'])

        # آلرت از بدترین سطح میان V، W و اعتبار خام X ساخته می‌شود
        causes = {'invalid': [], 'questionable': []}
        for code in ('v', 'w'):
            report = score.get(code)['report']
            if report in causes:
                causes[report].append(code)
        raw_x = score.get('x')['raw']
        if not d.X_VALID_MIN <= raw_x <= d.X_VALID_MAX:
            causes['invalid'].append('x')

        for level in ('invalid', 'questionable'):
            if causes[level]:
                score.set('validity', {'alert': level, 'reason': ','.join(causes[level])})
                return
        score.set('validity', {'alert': 'valid', 'reason': ''})

    # خط برش ترسیم پروفایل روی BR نهایی (بخش «ترسیم پروفایل» سند)
    def scoring_levels(self, score):
        for codes, bands in ((d.personality, d.personality_level),
                             (d.clinical, d.clinical_level),
                             (d.facets, d.facet_level),
                             (('x', 'y', 'z'), d.modifying_level)):
            for code in codes:
                obj = score.get(code)
                obj['level'] = self._level(bands, obj['br'])

    # کد مقیاس‌های شخصیت با BR نهایی ۷۵ و بالاتر، به ترتیب نمره
    def scoring_high_point(self, score):
        elevated = [c for c in d.personality
                    if score.get(c)['br'] >= d.HIGH_POINT_CUT]
        # elevated در ترتیب جدول پیوست ۳ ساخته شده و sort پایدار است، پس
        # نمرات تکراری خودبه‌خود «از بالا به پایین» گزارش می‌شوند.
        elevated.sort(key=lambda c: -score.get(c)['br'])
        score.set('high_point', ' '.join(c.upper() for c in elevated[:d.HIGH_POINT_MAX]))

    @staticmethod
    def _answer(item):
        try:
            answer = int(item.get('user_answered'))
        except (TypeError, ValueError):
            return None
        return answer if answer in (d.TRUE, d.FALSE) else None

    @staticmethod
    def _inconsistency(answers):
        total = 0
        for first, second in d.w_pairs:
            one, two = answers.get(first), answers.get(second)
            if one is not None and two is not None:
                total += abs(one - two)
        return total

    @staticmethod
    def _noteworthy(answers, code):
        true_items, false_items = d.noteworthy[code]
        raw = (sum(answers.get(q) == d.TRUE for q in true_items) +
               sum(answers.get(q) == d.FALSE for q in false_items))
        return {'raw': raw, 'percentage': round(raw / d.noteworthy_max[code], 4)}

    @classmethod
    def _set_br(cls, score, code, table):
        obj = score.get(code)
        obj['br'] = cls._lookup(table, obj['raw'])

    @staticmethod
    def _lookup(table, key):
        """جست‌وجو در جدول با چسباندن به نزدیک‌ترین کران در صورت نبود ردیف.

        این حالت سه جا پیش می‌آید: سقف نمره خام مقیاس‌های SS و CC در پیوست ۴،
        سقف ابعاد 4A.3، 4B.2، S.1 و S.2 در پیوست ۱۳، و بازه‌های ۰-۶ و ۱۱۵-۱۲۱
        نمره خام X که پیوست‌های ۵ و ۶ ردیفی برایشان ندارند (آزمون نامعتبر است).
        """
        if key in table:
            return table[key]
        keys = sorted(table)
        return table[keys[0]] if key < keys[0] else table[keys[-1]]

    @staticmethod
    def _shift(score, codes, weight):
        if not weight:
            return
        for code in codes:
            obj = score.get(code)
            obj['br'] = min(d.BR_MAX, max(d.BR_MIN, obj['br'] + weight))

    @staticmethod
    def _level(bands, value):
        for ceiling, report in bands:
            if value <= ceiling:
                return report
        return bands[-1][1]
