from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.CDRISC93 as dictionary

class CDRISC93(Data):
    scores = {'raw' :  None }

    # Five factor scores, each as {raw, percent} → `<factor>_raw`, `<factor>_percent`.
    # `percent` is the share of the factor's own maximum (raw / max), a fraction
    # kept to 3 decimals with halves rounded up — the same rounding MySQL applies
    # when the stored rows were backfilled, so old and new results agree.
    def scoring_raw(self, score):
        raws = dict.fromkeys(dictionary.factors_names, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    raws[factor] += answer - 1
            except:
                pass

        for factor in dictionary.factors_names:
            percent = (Decimal(raws[factor]) / Decimal(dictionary.maxes[factor])).quantize(
                Decimal('0.001'), rounding=ROUND_HALF_UP)
            score.set(factor, {
                'raw': raws[factor],
                'percent': float(percent),
            })
