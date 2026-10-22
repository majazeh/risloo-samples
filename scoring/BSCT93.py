from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.BSCT93 as dictionary

# BSCT — پرسشنامه خودپنداره بک. 25 items, five options each. Option 1..5 scores 5..1;
# the reversed items in scoring/dictionary/BSCT93.py score as chosen (1..5).
#   intellectual_ability    = 5 items  ( 5..25)
#   physical_attractiveness = 5 items  ( 5..25)
#   virtues                 = 5 items  ( 5..25)
#   work_efficacy           = 4 items  ( 4..20)
#   social_skills           = 6 items  ( 6..30)
#   total                   = all 25 items (25..125)
# Items per factor are in scoring/dictionary/BSCT93.py.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'intellectual_ability': 25,
    'physical_attractiveness': 25,
    'virtues': 25,
    'work_efficacy': 20,
    'social_skills': 30,
    'total': 125,
}


class BSCT93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                if i + 1 in dictionary.reverse_scoring_numbers:
                    answer = int(item.get('user_answered'))
                else:
                    answer = 6 - int(item.get('user_answered'))
                for factor in dictionary.factors[i + 1]:
                    raws[factor] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
