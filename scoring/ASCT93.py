from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.ASCT93 as dictionary

# ASCT — پرسش‌نامه خلاقیت عابدی. 60 items, three options each, scored 0, 1, 2
# (option number − 1); no reversed item.
#   fluency      = items  1..22  (0..44)
#   elaboration  = items 23..33  (0..22)
#   originality  = items 34..49  (0..32)
#   flexibility  = items 50..60  (0..22)
#   total        = all 60 items  (0..120)
# Items per factor are in scoring/dictionary/ASCT93.py.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decisions, 2026-10-13 and 2026-10-21. It is not a norm. It replaces the former
# `percentage` (0..100, one decimal, over the answered items only).
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum.
# No level and no alert is produced.

MAXES = {
    'total': 120,
    'fluency': 44,
    'elaboration': 22,
    'originality': 32,
    'flexibility': 22,
}


class ASCT93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered')) - 1
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
