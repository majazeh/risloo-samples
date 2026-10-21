from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.PNI93 as dictionary

# PNI — پرسشنامه خودشیفتگی مرضی پینکس. 52 items, options 1..6 scored as chosen; no reversed item.
#   contingent_self_esteem            = 12 items  (12..72)
#   exploitativeness                  =  5 items  ( 5..30)
#   self_sacrificing_self_enhancement =  6 items  ( 6..36)
#   hiding_the_self                   =  7 items  ( 7..42)
#   grandiose_fantasy                 =  7 items  ( 7..42)
#   devaluing                         =  7 items  ( 7..42)
#   entitlement_rage                  =  8 items  ( 8..48)
#   total                             = all 52 items (52..312)
# Items per factor are in scoring/dictionary/PNI93.py.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'contingent_self_esteem': 72,
    'exploitativeness': 30,
    'self_sacrificing_self_enhancement': 36,
    'hiding_the_self': 42,
    'grandiose_fantasy': 42,
    'devaluing': 42,
    'entitlement_rage': 48,
    'total': 312,
}


class PNI93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                raws['total'] += answer
                factor = dictionary.factors[i + 1]
                raws[factor] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
