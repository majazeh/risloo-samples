from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.CAQ93 as dictionary

# CAQ — آزمون اضطراب کتل. 40 items, three options each. The keyed option (1 or 3, per item,
# in scoring/dictionary/CAQ93.py) scores 2, the middle option scores 1, the other scores 0.
#   c               =  6 items  (0..12)
#   l               =  4 items  (0..8)
#   o               = 12 items  (0..24)
#   q3              =  8 items  (0..16)
#   q4              = 10 items  (0..20)
#   hidden_anxiety  = items 1..20   (0..40)
#   obvious_anxiety = items 21..40  (0..40)
#   total           = all 40 items  (0..80)
#
# Each raw score is returned as `<factor>_raw` and `<factor>_percent`. percent is the share of
# the score's own fixed maximum (raw / max), a fraction 0..1 kept to 3 decimals with halves
# rounded up, computed with Decimal — researcher's decision. It is not a norm.
# The keys are flat because `c`, `l`, `o`, `q3`, `q4` and `result` keep the standard (sten)
# scores, unchanged, next to them; `anxiety_level` is unchanged too.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; every raw
# score is returned, 0 when nothing was added. No alert is produced.

MAXES = {
    'c': 12,
    'l': 8,
    'o': 24,
    'q3': 16,
    'q4': 20,
    'hidden_anxiety': 40,
    'obvious_anxiety': 40,
    'total': 80,
}


class CAQ93(Data):
    scores = {'raw': None, 'norm': None}

    def scoring_raw(self, score):
        raws = dict.fromkeys(MAXES, 0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                continue

            key = i + 1
            factor = dictionary.factors.get(key)
            weight = 2 if answer == factor[1] else (1 if answer == 2 else 0)
            raws[factor[0]] += weight
            raws['total'] += weight
            raws['hidden_anxiety' if key <= 20 else 'obvious_anxiety'] += weight

        for name, top in MAXES.items():
            score.set(name + '_raw', raws[name])
            score.set(name + '_percent', percent(raws[name], top))

    def scoring_norm(self, score):
        gender = 'woman' if self.prerequisite('gender', 'user_answered') == 1 else 'man'
        result = score.get('total_raw')
        for key in dictionary.norm:
            if(result >= dictionary.norm[key][gender]):
                score.set('result', key)
                break
        level = 0
        result = score.get('result')
        if(result <= 3): level = 0
        elif(result <= 6): level = 1
        elif(result <= 7): level = 2
        else: level = 3
        score.set('anxiety_level', level)
        for factor in ['c', 'l', 'o', 'q3', 'q4']:
            score.set(factor, self.find_norm(score.get(factor + '_raw'), factor))


    def find_norm(self, raw, factor):
        i = 0
        while i < len(dictionary.norms[factor]):
            if (dictionary.norms[factor][i] != None):
                if(raw >= dictionary.norms[factor][i]):
                    return 10 - i
            i += 1


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
