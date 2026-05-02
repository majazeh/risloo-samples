from Data import Data
import scoring.dictionary.FRHPT9A as dictionary

class FRHPT9A(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        factors = {}
        for fi in dictionary.factor_list:
            factors[fi] = {'raw': 0, 'count': 0}

        median = 0
        none_median = 0

        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                continue

            if answer == 3 or answer == 4:
                median += 1
            if answer == 1 or answer == 6:
                none_median += 1

            index = i + 1
            s = (7 - answer) if index in dictionary.reverse_scoring_numbers else answer
            for factor in dictionary.factors.get(index, ()):
                factors[factor]['raw'] += s
                factors[factor]['count'] += 1

        result_factors = {}
        for key in factors:
            raw = factors[key]['raw']
            count = factors[key]['count']
            percentage = round(raw / (count * 6), 4) if count > 0 else 0
            result_factors[key] = {
                'raw': raw,
                'percentage': percentage,
                'level': self.getLevel(key, raw),
            }
        score.set('factors', result_factors)

        vi, vr = self.vrin()
        li, lr = self.lie_scale()
        di, dr = self.defensiveness_scale(result_factors)
        mi, mr = self.midpoint_responses(median, none_median)
        score.set('indicators', {
            'validity': {
                'median': {
                    'value': median,
                    'error': 'exceeded median response threshold' if median >= 21 else None
                }
            },
            'vrin': {'value': vi, 'level': vr},
            'lie_scale': {'value': li, 'level': lr},
            'defensiveness_scale': {'value': di, 'level': dr},
            'midpoint_responses': {'value': mi, 'level': mr},
        })

    def getLevel(self, key, raw):
        mean, sd = dictionary.norms[key]
        if raw >= round(mean + sd * 2, 3):
            return 'extremely_high'
        elif raw >= round(mean + sd * 1.5, 3):
            return 'very_high'
        elif raw >= round(mean + sd * 0.75, 3):
            return 'high'
        elif raw > round(mean - sd * 0.75, 3):
            return 'average'
        elif raw > round(mean - sd * 1.5, 3):
            return 'low'
        elif raw > round(mean - sd * 2, 3):
            return 'very_low'
        else:
            return 'extremely_low'

    def vrin(self):
        diffs = 0
        for fi, si in dictionary.doubles:
            items = self.get_items_entirely()
            f_ans = int(items[fi - 1].get('user_answered'))
            s_ans = int(items[si - 1].get('user_answered'))
            diffs += abs(f_ans - s_ans)
        if diffs >= 12:
            report = 'extremely_low'
        elif diffs >= 9:
            report = 'very_low'
        elif diffs >= 6:
            report = 'low'
        elif diffs >= 4:
            report = 'average'
        elif diffs >= 3:
            report = 'high'
        elif diffs == 2:
            report = 'very_high'
        else:
            report = 'extremely_high'
        return [diffs, report]

    def lie_scale(self):
        score = 0
        items = self.get_items_entirely()
        for v in dictionary.lie_scale:
            score += int(items[v - 1].get('user_answered'))
        if score >= 17:
            report = 'extremely_high'
        elif score >= 16:
            report = 'very_high'
        elif score >= 13:
            report = 'high'
        elif score >= 10:
            report = 'average'
        elif score >= 8:
            report = 'low'
        elif score == 6:
            report = 'very_low'
        else:
            report = 'extremely_low'
        return [score, report]

    def defensiveness_scale(self, factors):
        score = 0
        for key, value in dictionary.defensiveness_scale.items():
            raw = factors[key]['raw']
            if value > 0 and raw >= value:
                score += 1
            elif value < 0 and raw <= abs(value):
                score += 1
        if score >= 35:
            report = 'extremely_high'
        elif score >= 30:
            report = 'very_high'
        elif score >= 25:
            report = 'high'
        elif score >= 17:
            report = 'average'
        elif score >= 14:
            report = 'low'
        elif score == 10:
            report = 'very_low'
        else:
            report = 'extremely_low'
        return [score, report]

    def midpoint_responses(self, m, n):
        score = max(0, m - n)
        if score >= 33:
            report = 'extremely_high'
        elif score >= 30:
            report = 'very_high'
        elif score >= 24:
            report = 'high'
        elif score >= 16:
            report = 'average'
        elif score >= 13:
            report = 'low'
        elif score >= 8:
            report = 'very_low'
        else:
            report = 'extremely_low'
        return [score, report]
