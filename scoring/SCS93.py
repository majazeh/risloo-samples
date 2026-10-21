from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SCS93 as dictionary

# SCS — مقیاس خودکنترلی تانجنی، فرم ۳۶ سوالی. 36 items, options 1..5, where option 1 is
# «همیشه در مورد من صدق می‌کند» and option 5 «به هیچ وجه …». The 24 items in
# dictionary.reversed_scoring_numbers are scored as the option number (1..5), the other 12 as
# 6 - option (5..1). A higher score means more self-control, as in the operational plan —
# researcher's decision, 2026-10-21; until then the direction was the other way round.
#   capacity_self_discipline = items 2, 4, 5, 8, 9, 13, 15, 16, 17, 22, 24        (11..55)
#   deliberate_action        = items 11, 12, 14, 19, 20, 25, 31, 32, 33, 34       (10..50)
#   healthy_habits           = items 1, 6, 26, 27, 35                             (5..25)
#   work_ethics              = items 3, 23, 28, 29, 30                            (5..25)
#   reliability              = items 7, 10, 18, 21, 36                            (5..25)
#   total                    = all 36 items                                       (36..180)
# The items of each factor are in dictionary.factors.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the score's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'capacity_self_discipline': 55,
    'deliberate_action': 50,
    'healthy_habits': 25,
    'work_ethics': 25,
    'reliability': 25,
    'total': 180,
}


class SCS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i + 1 not in dictionary.reversed_scoring_numbers:
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
