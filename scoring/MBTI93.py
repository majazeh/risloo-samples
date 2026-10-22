from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.MBTI93 as dictionary

# MBTI — آزمون تیپ‌نمای مایرز-بریگز، فرم ۸۷سؤالی. 87 two-option items; each option adds a
# weight of 0, 1 or 2 to one pole, as listed in scoring/dictionary/MBTI93.py (option 1 of
# item 10 adds to no pole). Eight pole scores, each the weighted count of its own options:
#   e  items  1..25  (0..35)    i  items  1..25  (0..34)
#   s  items 26..50  (0..33)    n  items 26..50  (0..31)
#   t  items 51..75  (0..35)    f  items 51..75  (0..30)
#   j  items 76..87  (0..19)    p  items 76..87  (0..18)
# The two poles of a pair do not add up to a constant, so each pole is a score of its own.
#
# Each pole is returned as {raw, percent}, which Risloo flattens to `<pole>_raw` and
# `<pole>_percent`. percent is the share of the pole's own fixed maximum (raw / max),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# The raw score of each pole is also returned under its old single-letter key (E, I, …),
# which keeps the old `e` … `p` columns filled for 87-item results.
#
# `report` is the four-letter type and is not a percent score. It is decided on raw scores,
# unchanged from before: for each pair the pole with the higher raw score gives the letter;
# on a tie both letters are kept in parentheses, e.g. (EI)STJ.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; a pole
# with nothing added is still returned (raw 0, percent 0.0). No alert is produced.

MAXES = {
    'e': 35,
    'i': 34,
    's': 33,
    'n': 31,
    't': 35,
    'f': 30,
    'j': 19,
    'p': 18,
}


class MBTI93(Data):
    scores = {'raw': None, 'report': None}

    def scoring_raw(self, score):
        self.raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            if item.get('user_answered') == None: continue
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[answer][i + 1]
                self.raws[factor[0].lower()] += factor[1]
            except:
                pass

        for name, top in MAXES.items():
            score.set(name, {'raw': self.raws[name], 'percent': percent(self.raws[name], top)})

        # The old single-letter keys, as before (E, I, S, N, T, F, J, P): they still fill the
        # old `e` … `p` columns, which the old MBTI-93 profile in Risloo reads.
        # Every pole is present; a pole with no points is 0, the old columns' default.
        for name in MAXES:
            score.set(name.upper(), self.raws[name])

    def scoring_report(self, score):
        report = ''
        for first, second in dictionary.factors_group:
            a = self.raws[first.lower()]
            b = self.raws[second.lower()]
            if a == b:
                report += '(' + first + second + ')'
            elif a > b:
                report += first
            else:
                report += second
        score.set('report', report)


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
