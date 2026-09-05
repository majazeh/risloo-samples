from Data import Data
import scoring.dictionary.JSS93 as dictionary


class JSS93(Data):
    scores = {'raw': None}

    # 9 factor scores + the total, each as {raw, percentage}.
    #
    # Reverse items are recoded `6 - answer` (scoring doc §1/§4); direct items keep
    # their answer. JSS is all-or-nothing: the document forbids imputation and says
    # an incomplete form must not be scored, so a missing or out-of-range answer
    # aborts scoring instead of being silently skipped like in most other scales.
    #
    # `percentage` is the share of the possible maximum (raw / max), which is the
    # definition the profile design uses (raw 4 of 20 → 20 %, 102 of 180 → 57 %).
    def scoring_raw(self, score):
        raws = dict.fromkeys(dictionary.factors_names, 0)
        answered = set()

        for i, item in self.items():
            index = i + 1
            if index not in dictionary.factors:
                continue

            answer = self._answer(item, index)
            if index in dictionary.reverse_scoring_numbers:
                answer = dictionary.options + 1 - answer

            for factor in dictionary.factors[index]:
                raws[factor] += answer
            answered.add(index)

        missing = sorted(set(dictionary.factors) - answered)
        if missing:
            raise ValueError('JSS93 has no answer for item(s) {}'.format(missing))

        for factor in dictionary.factors_names:
            score.set(factor, {
                'raw': raws[factor],
                # Kept as a 3-decimal fraction so the reported percentage still
                # carries the one decimal the scoring document asks for.
                'percentage': round(raws[factor] / dictionary.maxes[factor], 3),
            })

    @staticmethod
    def _answer(item, index):
        try:
            answer = int(item.get('user_answered'))
        except (TypeError, ValueError):
            raise ValueError('JSS93 item {} is unanswered'.format(index))

        if not 1 <= answer <= dictionary.options:
            raise ValueError('JSS93 item {} answer {} is outside 1..{}'.format(
                index, answer, dictionary.options))

        return answer
