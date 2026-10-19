from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.JPSDI93 as dictionary

class JPSDI93(Data):
    scores = {'raw' :  None }

    # Four stage scores, each as {raw, percent} → `<stage>_raw`, `<stage>_percent`.
    # `percent` is the share of the stage's own maximum (raw / 15), a fraction
    # kept to 3 decimals with halves rounded up — the same rounding MySQL applies
    # when the stored rows were backfilled, so old and new results agree.
    def scoring_raw(self, score):
        raws = dict.fromkeys(dictionary.factors_names, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[i + 1][answer]
                raws[factor] += 1
            except:
                pass

        for factor in dictionary.factors_names:
            percent = (Decimal(raws[factor]) / Decimal(dictionary.maxes[factor])).quantize(
                Decimal('0.001'), rounding=ROUND_HALF_UP)
            score.set(factor, {
                'raw': raws[factor],
                'percent': float(percent),
            })

        # `total` (researcher decision, 2026-10-19): each stage count times its
        # stage number, 15–60 on a complete sheet → `total_raw`, `total_percent`.
        total = sum(dictionary.weights[f] * raws[f] for f in dictionary.factors_names)
        score.set('total', {
            'raw': total,
            'percent': float((Decimal(total) / Decimal(dictionary.total_max)).quantize(
                Decimal('0.001'), rounding=ROUND_HALF_UP)),
        })

        # `psdi`: the stage(s) with the highest raw score, comma-joined on a tie,
        # named by stage (`level_2,level_3`) as in results stored before.
        top = max(raws.values())
        score.set('psdi', ','.join(f for f in dictionary.factors_names if raws[f] == top))
