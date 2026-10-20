from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SPWB93 as dictionary

# SPWB — پرسشنامه بهزیستی روان‌شناختی ریف، 54 items, options 1..6; the 28 items in
# dictionary.reverse_scoring_numbers are reversed (7 - answer).
#   self_acceptance                = 9 items   (9..54)
#   positive_reactions_with_others = 9 items   (9..54)
#   autonomy                       = 9 items   (9..54)
#   environmental_mastery          = 9 items   (9..54)
#   purpose_in_life                = 9 items   (9..54)
#   personal_growth                = 9 items   (9..54)
#   total                          = all 54 items (54..324)
# The items of each factor are in dictionary.items.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'self_acceptance': 54,
    'positive_reactions_with_others': 54,
    'autonomy': 54,
    'environmental_mastery': 54,
    'purpose_in_life': 54,
    'personal_growth': 54,
    'total': 324,
}


class SPWB93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i + 1 in dictionary.reverse_scoring_numbers:
                    answer = 7 - answer
                factor = dictionary.items.get(i + 1)
                raws['total'] += answer
                raws[factor] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
