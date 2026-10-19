from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.PSOC93 as dictionary

class PSOC93(Data):
    scores = {'raw' :  None }

    # Two factor scores, each as {raw, percent} → `<factor>_raw`, `<factor>_percent`.
    # `percent` is the share of the factor's own maximum (raw / max), a fraction
    # kept to 2 decimals (the most the data store keeps) with halves rounded up —
    # the same rounding MySQL applies when the stored rows were backfilled, so old
    # and new results agree.
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        raws = dict.fromkeys(dictionary.factors_names, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factors = dictionary.factors[i + 1]
                if i+1 in dictionary.reverse_scoring_numbers:
                    answer = option_numbers + 1 - answer
                for factor in factors:
                    raws[factor] += answer
            except:
                pass

        for factor in dictionary.factors_names:
            percent = (Decimal(raws[factor]) / Decimal(dictionary.maxes[factor])).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP)
            score.set(factor, {
                'raw': raws[factor],
                'percent': float(percent),
            })
