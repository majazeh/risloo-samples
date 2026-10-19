from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.TMPS93 as dictionary

class TMPS93(Data):
    scores = {'raw' :  None }

    # Three factors and the total, each as {raw, percent} → `<factor>_raw`, `<factor>_percent`.
    # Option 1 (کاملا موافقم) scores 5 … option 5 (کاملاً مخالفم) scores 1; no reverse items.
    # `percent` is the share of the factor's own maximum (raw / max), a fraction
    # kept to 3 decimals with halves rounded up.
    def scoring_raw(self, score):
        raws = dict.fromkeys(dictionary.factors_names, 0)
        for i, item in self.items():
            try:
                answer = 6 - int(item.get('user_answered'))
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    raws[factor] += answer
            except:
                pass

        for factor in dictionary.factors_names:
            percent = (Decimal(raws[factor]) / Decimal(dictionary.maxes[factor])).quantize(
                Decimal('0.001'), rounding=ROUND_HALF_UP)
            score.set(factor, {
                'raw': raws[factor],
                'percent': float(percent),
            })
