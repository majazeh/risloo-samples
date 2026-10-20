from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.MWAS93 as dictionary

# Eight factors in dictionary order, then the total; each is {raw, percent}, which Risloo
# flattens to `<factor>_raw`, `<factor>_percent` (`total_raw`, `total_percent`).
# Option 1 (کاملاً موافقم) scores 5 … option 5 (کاملاً مخالفم) scores 1; reverse items keep the option number.
# `percent` is the share of the factor's own fixed maximum (items × 5; total 36 × 5 = 180),
# a fraction kept to 3 decimals with halves rounded up. An unanswered item adds nothing.
FACTORS = dictionary.factors_names[:8]
MAXES = {factor: 5 * sum(1 for fs in dictionary.factors.values() if factor in fs) for factor in FACTORS}
MAXES['total'] = 5 * len(dictionary.factors)


def percent(raw, maximum):
    return float((Decimal(raw) / Decimal(maximum)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))


class MWAS93(Data):
    scores = {'raw' :  None }

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i+1 not in dictionary.reversed_scoring_numbers:
                    answer = 6 - answer
                factors = dictionary.factors[i + 1]
                raws['total'] += answer
                for factor in factors:
                    raws[factor] += answer
            except:
                pass

        for factor in MAXES:
            score.set(factor, {
                'raw': raws[factor],
                'percent': percent(raws[factor], MAXES[factor]),
            })
