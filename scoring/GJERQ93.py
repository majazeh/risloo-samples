from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.GJERQ93 as dictionary

# GJERQ — پرسشنامه تنظیم هیجان گراس و جان. 10 items, options 1..7 (کاملا مخالفم .. کاملا موافقم);
# no reversed item.
#   cognitive_reappraisal = items 1, 3, 5, 7, 8, 10    (6..42)
#   suppression           = items 2, 4, 6, 9           (4..28)
#   total                 = all 10 items               (10..70)
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {'total': 70, 'cognitive_reappraisal': 42, 'suppression': 28}


class GJERQ93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[i + 1]
                raws['total'] += answer
                raws[factor] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
