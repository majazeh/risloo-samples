from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SRQ93 as dictionary

# SRQ — پرسشنامه خودنظم‌جوی بوفارد. 13 items, options 1..5; items 5, 10, 13 are reversed (6 - answer).
#   cognition     = items 4, 7, 8, 9               (4..20)
#   metacognition = items 1, 2, 3, 6, 11, 12       (6..30)
#   motivation    = items 5, 10, 13                (3..15)
#   total         = all 13 items                   (13..65)
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {'cognition': 20, 'metacognition': 30, 'motivation': 15, 'total': 65}


class SRQ93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i + 1 in dictionary.reversed_scoring_numbers:
                    answer = 6 - answer
                factors = dictionary.factors[i + 1]
                raws['total'] += answer
                for factor in factors:
                    raws[factor] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
