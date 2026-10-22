from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.DASS9A as dictionary
import scoring.dictionary.DASS as g_dictionary

# DASS — آزمون مقیاس افسردگی، اضطراب، استرس، فرم بلند (DASS9A). 42 items, options 1..4
# («به هیچ وجه در مورد من صادق نیست.» .. «بسیار زیاد در مورد من صادق است.») worth 0..3
# (option - 1), no reversed item.
#   depression = items 3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42     (0..42)
#   anxiety    = items 2, 4, 7, 9, 15, 19, 20, 23, 25, 28, 30, 36, 40, 41       (0..42)
#   stress     = items 1, 6, 8, 11, 12, 14, 18, 22, 27, 29, 32, 33, 35, 39      (0..42)
# The items of each factor are in dictionary.factors.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of this form's fixed maximum (raw / 42), a
# fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-21. It is not a norm. The short form (DASS93) shares the
# score table but has its own maximum (21).
#
# intensity is unchanged: the raw is placed in the bands of g_dictionary.factors_interval
# (0 normal .. 4 extremely severe); Risloo stores it as `intensity_<factor>`.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAX = 42


class DASS9A(Data):
    scores = {'raw': None, 'report': 'intensity'}

    def scoring_raw(self, score):
        self.raws = dict.fromkeys(g_dictionary.factors_names, 0)
        for i, item in self.items():
            if(item.get('user_answered') == None): continue
            try:
                answer = int(item.get('user_answered')) - 1
                factor = dictionary.factors[i + 1]
                if factor:
                    self.raws[factor] += answer
            except:
                pass

        for factor in g_dictionary.factors_names:
            raw = self.raws[factor]
            score.set(factor, {'raw': raw, 'percent': percent(raw, MAX)})

    def scoring_report(self, score):
        for factor in g_dictionary.factors_names:
            interval_dict = g_dictionary.factors_interval[factor]
            factor_value = self.raws[factor]

            intensity = self.get_intensity(factor_value, interval_dict)
            score.set(factor, intensity)

    def get_intensity(self, factor_value, interval_dict):
        intervals = list(interval_dict.keys())
        for interval in intervals:
            if len(interval) == 2:
                if interval[0] <= factor_value <= interval[1]:
                    return interval_dict[interval]

            else:
                return interval_dict[interval]


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
