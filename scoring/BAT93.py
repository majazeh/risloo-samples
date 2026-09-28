from Data import Data
import scoring.dictionary.BAT93 as dictionary


class BAT93(Data):
    scores = {'raw': None}

    # Six reportable scales plus the two secondary subscales, each as
    # {raw, score, level}.
    #
    # `raw` is the plain sum of the items (the profile prints it as "raw / max").
    # `score` is the official interpretive figure: the *mean* of the items, 1.00-5.00
    # rounded to two decimals (scoring doc §2). `level` is the Flemish clinical
    # cut-off class read off that rounded mean: 1 = سبز, 2 = نارنجی, 3 = قرمز, and
    # 0 for the two secondary subscales, which have no published cut-off.
    #
    # No item is reverse scored. The document declares every item mandatory, so a
    # missing or out-of-range answer aborts scoring instead of being skipped.
    def scoring_raw(self, score):
        raws = dict.fromkeys(dictionary.factors_names, 0)
        answered = set()

        for i, item in self.items():
            index = i + 1
            if index not in dictionary.factors:
                continue

            answer = self._answer(item, index)
            for factor in dictionary.factors[index]:
                raws[factor] += answer
            answered.add(index)

        missing = sorted(set(dictionary.factors) - answered)
        if missing:
            raise ValueError('BAT93 has no answer for item(s) {}'.format(missing))

        for factor in dictionary.factors_names:
            raw = raws[factor]
            mean = self._mean(raw, dictionary.counts[factor])
            score.set(factor, {
                'raw': raw,
                'score': mean,
                'level': self._level(mean, dictionary.cutoffs.get(factor)),
            })

    @staticmethod
    def _answer(item, index):
        try:
            answer = int(item.get('user_answered'))
        except (TypeError, ValueError):
            raise ValueError('BAT93 item {} is unanswered'.format(index))

        if not 1 <= answer <= dictionary.options:
            raise ValueError('BAT93 item {} answer {} is outside 1..{}'.format(
                index, answer, dictionary.options))

        return answer

    @staticmethod
    def _mean(raw, count):
        # Mean of the items on two decimals, rounded half up: exhaustion has eight
        # items, so raw/8 can land exactly on a half (25/8 = 3.125), and round() would
        # break that tie to even instead of upwards.
        return (2 * raw * 100 + count) // (2 * count) / 100.0

    @staticmethod
    def _level(mean, cutoff):
        # The cut-off table is written on two decimals (… 2.58 | 2.59 … 3.01 | 3.02 …),
        # so the rounded mean — the number the report shows — is what gets classified.
        if cutoff is None:
            return dictionary.LEVEL_NONE
        if mean <= cutoff[0]:
            return 1
        if mean <= cutoff[1]:
            return 2
        return 3
