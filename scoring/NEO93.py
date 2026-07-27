from Data import Data
import scoring.dictionary.NEO93 as d


class NEO93(Data):
    scores = {'raw': None, 'norm': None}

    # Raw scores + the four validity flags from inter.md + per-option counts + type.
    def scoring_raw(self, score):
        raw = {k: 0 for k in d.domains + d.facets}
        count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        voption = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
        vq = {q: None for q in d.VALIDITY_ITEMS}
        run_val, run_len = None, 0
        random_flag = False

        for i, item in self.items():
            index = i + 1
            if index in vq:                          # validity items (lenient)
                vq[index] = self._parse(item)
                continue
            if index > d.N_ITEMS:
                continue
            answer = self._parse(item)
            if answer is None:
                raise ValueError("NEO93 item {} unanswered or invalid".format(index))

            facet = d.factors[index]
            points = (5 - answer) if index in d.reverse else (answer - 1)
            raw[facet] += points
            if len(facet) > 1:                       # facet also rolls up into its domain
                raw[facet[0]] += points

            count[answer] += 1
            # Random responding: a consecutive run of one option reaching its
            # threshold "or more" trips both the per-option flag and the global one.
            if answer == run_val:
                run_len += 1
            else:
                run_val, run_len = answer, 1
            if run_len >= d.VOPTION_THRESHOLDS[answer]:
                voption[answer] = 0
                random_flag = True

        for k in d.domains + d.facets:
            score.set(k, {'raw': raw[k], 'score': None, 'level': None})
        score.set('type', d.TYPE)
        score.set('options', {str(v): {'count': count[v], 'v': voption[v]} for v in (1, 2, 3, 4, 5)})

        # validity: 1 = valid (matches the valid/invalid enum in the spec file).
        # The other three flags follow the yes/no enum: 1 = the condition holds.
        c45 = count[4] + count[5]
        score.set('validity', 0 if any(self._ve(vq[q], d.VE_ERROR[q]) for q in d.VALIDITY_ITEMS) else 1)
        score.set('acquiescence', 1 if c45 >= d.ACQUIESCENCE_MIN else 0)
        score.set('nay_saying', 1 if c45 <= d.NAY_SAYING_MAX else 0)
        score.set('random_responding', 1 if random_flag else 0)

    # Normalisation: score = proportion of the maximum (0..1), level = 1..5 read from the
    # gender-specific raw-score description table.
    def scoring_norm(self, score):
        # Age is an alert only - inter.md asks for an alert, not for scoring to stop.
        score.set('age_alert', 1 if self._lt(self.prerequisite('age'), d.AGE_MIN) else 0)

        # Table: woman(1) / men(2). The "total" table was dropped by the scientific
        # team, so gender is mandatory and scoring cannot continue without it.
        g = self.prerequisite('gender')
        g = g.get('user_answered') if g else None
        try:
            gender = int(g)
        except (TypeError, ValueError):
            gender = None
        if gender not in (1, 2):
            raise ValueError("NEO93 gender notfound")
        table = d.norm['woman' if gender == 1 else 'men']

        for k in d.domains + d.facets:
            obj = score.get(k)
            raw = obj['raw']
            obj['score'] = self._ratio(raw, d.maxes[k])
            obj['level'] = self._level(raw, table[k])

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
