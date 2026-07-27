from Data import Data
import scoring.dictionary.NEO9Q as d


class NEO9Q(Data):
    scores = {'raw': None, 'norm': None}

    # Raw scores + the four validity flags from the Haghshenas document
    # + per-option counts + type.
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
                raise ValueError("NEO9Q item {} unanswered or invalid".format(index))

            facet = d.factors[index]
            points = (5 - answer) if index in d.reverse else (answer - 1)
            raw[facet] += points
            if len(facet) > 1:                       # facet also rolls up into its domain
                raw[facet[0]] += points

            count[answer] += 1
            # Random responding: only options 1, 4 and 5 have a documented threshold
            # on this form; the other two never trip the flag.
            if answer == run_val:
                run_len += 1
            else:
                run_val, run_len = answer, 1
            if run_len >= d.VOPTION_THRESHOLDS.get(answer, 10 ** 9):
                voption[answer] = 0
                random_flag = True

        for k in d.domains + d.facets:
            score.set(k, {'raw': raw[k], 'score': None, 'level': None})
        score.set('type', d.TYPE)
        score.set('options', {str(v): {'count': count[v], 'v': voption[v]} for v in (1, 2, 3, 4, 5)})

        # validity: 1 = valid. The other three follow the yes/no enum: 1 = condition holds.
        c45 = count[4] + count[5]
        score.set('validity', 0 if any(self._ve(vq[q], d.VE_ERROR[q]) for q in d.VALIDITY_ITEMS) else 1)
        score.set('acquiescence', 1 if c45 >= d.ACQUIESCENCE_MIN else 0)
        score.set('nay_saying', 1 if c45 <= d.NAY_SAYING_MAX else 0)
        score.set('random_responding', 1 if random_flag else 0)

    # Normalisation: score = gender-specific T score, level = 1..5 from the T cut-offs.
    def scoring_norm(self, score):
        # Age is an alert only - the scientific team asked for an alert on every form,
        # with scoring still carried out.
        score.set('age_alert', 1 if self._lt(self.prerequisite('age'), d.AGE_MIN) else 0)

        # Gender stays mandatory: the T table cannot be selected without it.
        g = self.prerequisite('gender')
        g = g.get('user_answered') if g else None
        try:
            gender = int(g)
        except (TypeError, ValueError):
            gender = None
        if gender not in (1, 2):
            raise ValueError("NEO9Q gender notfound")
        table = d.norm['woman' if gender == 1 else 'men']

        for k in d.domains + d.facets:
            obj = score.get(k)
            t = self._lookup(table[k], obj['raw'])
            obj['score'] = t
            obj['level'] = self._level(t)

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
    def _lookup(factor_norm, raw):
        # Highest band whose lower bound the raw score reaches -> T score; floor 20.
        for lb in sorted(factor_norm, reverse=True):
            if raw >= lb:
                return factor_norm[lb]
        return 20

    @staticmethod
    def _level(t):
        if t < 35:
            return 1
        if t < 45:
            return 2
        if t < 55:
            return 3
        if t < 65:
            return 4
        return 5
