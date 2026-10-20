from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SISRI93 as dictionary

# SISRI — مقیاس هوش معنوی کینگ. 24 items, options 1..5 scored 5 - answer (4..0);
# item 6 is reversed (answer - 1).
#   critical_existential_thinking = items 1, 3, 5, 9, 13, 17, 21          (0..28)
#   personal_meaning_production   = items 7, 11, 15, 19, 23                (0..20)
#   transcendental_awareness      = items 2, 6, 10, 14, 18, 20, 22         (0..28)
#   conscious_state_expansion     = items 4, 8, 12, 16, 24                 (0..20)
#   total                         = all 24 items                           (0..96)
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'critical_existential_thinking': 28,
    'personal_meaning_production': 20,
    'transcendental_awareness': 28,
    'conscious_state_expansion': 20,
    'total': 96,
}


class SISRI93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i + 1 in dictionary.reversed_scoring_numbers:
                    answer = answer - 1
                else:
                    answer = 5 - answer
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
