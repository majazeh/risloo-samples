from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.GHGAQ93 as dictionary

# GHGAQ — پرسشنامه دلبستگی به خدا غباری بناب و حدادی. 16 items, options 1..5 scored as
# answered (1..5); items 10, 13, 14 are reversed (6 - answer).
#   try_to_closness          = items 1, 2              (2..10)
#   secure_haven             = items 3, 4, 5           (3..15)
#   secure_base              = items 6, 7, 8           (3..15)
#   objection_to_separation  = items 9, 10, 11         (3..15)
#   positive_self_perception = items 12, 13, 14        (3..15)
#   positive_god_perception  = items 15, 16            (2..10)
#   total                    = all 16 items            (16..80)
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm. The lowest possible score is not
# zero, so the lowest percent is 0.2, not 0.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'try_to_closness': 10,
    'secure_haven': 15,
    'secure_base': 15,
    'objection_to_separation': 15,
    'positive_self_perception': 15,
    'positive_god_perception': 10,
    'total': 80,
}


class GHGAQ93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[i + 1]
                if i + 1 in dictionary.reverse_scoring_numbers:
                    answer = 6 - answer
                raws[factor] += answer
                raws['total'] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
