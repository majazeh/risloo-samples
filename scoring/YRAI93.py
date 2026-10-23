from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.YRAI93 as dictionary

# YRAI — آزمون اجتناب یانگ و ریگ. 40 items, options 1..6 («کاملاً غلط» .. «کاملاً درست»)
# scored as chosen; no reversed item. Items 9, 13 and 40 count in two factors each.
#   intentionally_not_thinking_about_upsetting_things  = 3 items  (3..18)
#   substance_abuse                                    = 3 items  (3..18)
#   denial_of_unhappiness                              = 4 items  (4..24)
#   excessive_rationality_and_control                  = 5 items  (5..30)
#   suppression_of_anger                               = 3 items  (3..18)
#   psychosomatic_symptoms                             = 4 items  (4..24)
#   denial_of_memories                                 = 3 items  (3..18)
#   withdrawal_from_people                             = 3 items  (3..18)
#   avoidance_through_sleep_and_lack_of_energy         = 2 items  (2..12)
#   distraction_through_activity                       = 3 items  (3..18)
#   self_soothing_like_eating_shopping_etc             = 3 items  (3..18)
#   passive_blocking_of_upsetting_emotions             = 4 items  (4..24)
#   passive_distraction_fantasy_daydreaming_television = 2 items  (2..12)
#   avoidance_of_upsetting_situations                  = 1 item   (1..6)
# Items per factor are in scoring/dictionary/YRAI93.py; each maximum below is derived from
# it (items in the factor × 6). There is no total score.
#
# Each score is returned as {raw, percent}, which Risloo flattens to `<factor>_raw` and
# `<factor>_percent`. percent is the share of the factor's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-22. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a factor
# with no answered item is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    name: 6 * sum(name in factors for factors in dictionary.factors.values())
    for name in dictionary.factors_names
}


class YRAI93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                for factor in dictionary.factors[i + 1]:
                    raws[factor] += answer
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': raws[name], 'percent': percent(raws[name], top)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
