from Data import Data
import scoring.dictionary.NEO9A as d


class NEO9A(Data):
    scores = {'raw': None, 'norm': None}

    # Raw scores + validity + per-option counts + type.
    # Note: the Garousi short form has no random-responding / acquiescence /
    # nay-saying rule. inter.md only defines items 61..63 and the spec file only
    # asks for the validity column, so the per-option run flags always stay 1.
    def scoring_raw(self, score):
        raw = {k: 0 for k in d.domains + d.facets}
        count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        voption = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        vq = {q: None for q in d.VALIDITY_ITEMS}
        run_val, run_len = None, 0

        for i, item in self.items():
            index = i + 1
            if index in vq:                          # validity items (lenient)
                vq[index] = self._parse(item)
                continue
            if index > d.N_ITEMS:
                continue
            answer = self._parse(item)
            if answer is None:
                raise ValueError("NEO9A item {} unanswered or invalid".format(index))

            facet = d.factors[index]
            points = (5 - answer) if index in d.reverse else (answer - 1)
            raw[facet] += points
            if len(facet) > 1:                       # this form has no facets
                raw[facet[0]] += points

            count[answer] += 1
            # Counts are stored for every form; run flags only fire where the source
            # document defines a threshold, which this form does not.
            if answer == run_val:
                run_len += 1
            else:
                run_val, run_len = answer, 1
            if run_len >= d.VOPTION_THRESHOLDS.get(answer, 10 ** 9):
                voption[answer] = 0

        for k in d.domains + d.facets:
            score.set(k, {'raw': raw[k], 'score': None, 'level': None})
        score.set('type', d.TYPE)
        score.set('options', {str(v): {'count': count[v], 'v': voption[v]} for v in (1, 2, 3, 4, 5)})
        # validity: 1 = valid, 0 = invalid.
        score.set('validity', 0 if any(self._ve(vq[q], d.VE_ERROR[q]) for q in d.VALIDITY_ITEMS) else 1)

    # Normalisation: score = proportion of the maximum (0..1), level = 1..5 from the
    # non-gendered raw-score description table (attachment 5).
    def scoring_norm(self, score):
        for k in d.domains + d.facets:
            obj = score.get(k)
            raw = obj['raw']
            obj['score'] = self._ratio(raw, d.maxes[k])
            obj['level'] = self._level(raw, d.norm[k])

    @staticmethod
    def _parse(item):
        try:
            a = int(item.get('user_answered'))
        except (TypeError, ValueError):
            return None
        return a if 1 <= a <= 5 else None

    @staticmethod
    def _ve(answer, error_set):
        # 1 = validity error (answer is in the error set), 0 = clean or unanswered.
        return 1 if (answer is not None and answer in error_set) else 0

    @staticmethod
    def _ratio(raw, m):
        # Proportion of the maximum, 3 decimals, rounded half up: 5 of 10 -> 0.5.
        # Column type is decimal(6,3), which also holds the NEO9Q T score (up to 80.000).
        return (2 * raw * 1000 + m) // (2 * m) / 1000

    @staticmethod
    def _level(raw, th):
        if raw <= th[0]:
            return 1
        if raw <= th[1]:
            return 2
        if raw <= th[2]:
            return 3
        if raw <= th[3]:
            return 4
        return 5
