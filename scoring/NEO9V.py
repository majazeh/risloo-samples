from Data import Data
import scoring.dictionary.NEO9V as d


class NEO9V(Data):
    scores = {'raw': None, 'norm': None}

    # Raw scores + validity + per-option counts + type.
    # Validity has two sources on this form (inter.md): the answers to items 61..63,
    # and a count of ten or more "no opinion" answers. Either one invalidates the test.
    # The neutral count is not emitted separately - it is options.3.count.
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
                raise ValueError("NEO9V item {} unanswered or invalid".format(index))

            points = (5 - answer) if index in d.reverse else (answer - 1)
            raw[d.factors[index]] += points          # domain
            facet = d.subfactors.get(index)          # subscale (items 28 and 33 have none)
            if facet:
                raw[facet] += points

            count[answer] += 1
            # Counts are stored for every form; run flags only fire where the source
            # document defines a threshold, which this form does not.
            if answer == run_val:
                run_len += 1
            else:
                run_val, run_len = answer, 1
            if run_len >= d.VOPTION_THRESHOLDS.get(answer, 10 ** 9):
                voption[answer] = 0

        # level is fixed at NO_LEVEL (0) for this form: it has no norm table, and the
        # {f}_level column is NOT NULL so a null would be rejected on insert.
        for k in d.domains + d.facets:
            score.set(k, {'raw': raw[k], 'score': None, 'level': d.NO_LEVEL})
        score.set('type', d.TYPE)
        score.set('options', {str(v): {'count': count[v], 'v': voption[v]} for v in (1, 2, 3, 4, 5)})
        # validity: 1 = valid, 0 = invalid (failed validity item, or too many neutrals).
        ve = any(self._ve(vq[q], d.VE_ERROR[q]) for q in d.VALIDITY_ITEMS)
        score.set('validity', 0 if (ve or count[d.NEUTRAL_OPTION] >= d.NEUTRAL_MAX) else 1)

    # Normalisation: ratio only. This form has no norm table, so level is left at
    # NO_LEVEL and never computed.
    def scoring_norm(self, score):
        # Age is an alert only - the scientific team asked for an alert on every form,
        # with scoring still carried out.
        score.set('age_alert', 1 if self._lt(self.prerequisite('age'), d.AGE_MIN) else 0)

        for k in d.domains + d.facets:
            obj = score.get(k)
            obj['score'] = self._ratio(obj['raw'], d.maxes[k])

    @staticmethod
    def _parse(item):
        try:
            a = int(item.get('user_answered'))
        except (TypeError, ValueError):
            return None
        return a if 1 <= a <= 5 else None

    @staticmethod
    def _lt(prereq, limit):
        # True only when the prerequisite is present and below the limit.
        v = prereq.get('user_answered') if prereq else None
        try:
            return int(v) < limit
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _ve(answer, error_set):
        # 1 = validity error (answer is in the error set), 0 = clean or unanswered.
        return 1 if (answer is not None and answer in error_set) else 0

    @staticmethod
    def _ratio(raw, m):
        # Proportion of the maximum, 3 decimals, rounded half up: 5 of 10 -> 0.5.
        # This form has no norm table, so the proportion is what gets stored rather than
        # a level. Column type is decimal(6,3); 3 decimals keep every raw score of every
        # subscale distinct (smallest step is 1/32 = 0.031).
        return (2 * raw * 1000 + m) // (2 * m) / 1000
