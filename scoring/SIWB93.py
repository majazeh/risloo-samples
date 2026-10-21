from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SIWB93 as dictionary

# SIWB — پرسشنامه سنجش معنوی دلمن و فری. 12 items, options 1..5 scored as the option
# number (کاملا موافقم = 1 … کاملا مخالفم = 5); no item is reversed.
#   self_efficacy = items 1..6     (6..30)
#   life_scheme   = items 7..12    (6..30)
#   total         = all 12 items   (12..60)
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm. The lowest raw score is not 0, so
# the lowest percent is 0.2, not 0.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {'self_efficacy': 30, 'life_scheme': 30, 'total': 60}


class SIWB93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[i + 1]
                raws[factor] += answer
                raws['total'] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
