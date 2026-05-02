import random
from Data import Data
import scoring.dictionary.RIASEC9A as dictionary

class RIASEC9A(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        score.set(dictionary.factors_names, 0)
        data = {}
        for factor in dictionary.factors_names:
            data[factor] = 0

        for i, item in self.items():
            try:
                option = int(item.get('user_answered'))
                item_number = i + 1
                factors = dictionary.factors[item_number]
                if item_number <= 252:
                    answer = 1 if option == 1 else 0
                else:
                    answer = option
                for factor in factors:
                    data[factor] += answer
            except:
                pass

        # rank
        unique_sorted = sorted(set(data.values()))
        rank_map = {val: idx for idx, val in enumerate(unique_sorted, start=7 - len(unique_sorted))}

        # congruence — hexagon order: R, I, A, S, E, C
        hexagon = list(dictionary.factors_names)
        max_rank = max(rank_map[data[f]] for f in dictionary.factors_names)
        top_positions = [hexagon.index(f) for f in dictionary.factors_names if rank_map[data[f]] == max_rank]

        for factor in dictionary.factors_names:
            raw = data[factor]
            rank = rank_map[raw]
            pos = hexagon.index(factor)
            min_dist = min(min(abs(pos - tp), 6 - abs(pos - tp)) for tp in top_positions)
            congruence = 4 - min_dist
            score.set(factor, {
                'raw': raw,
                'percentage': round(raw / 56, 4),
                'rank': rank,
                'congruence': congruence,
                'calibrated': rank + congruence
            })

        # three-letter code
        calibrated = {f: score.get(f)['calibrated'] for f in dictionary.factors_names}
        slots = []
        alert = False
        used = set()
        for cal_val in sorted(set(calibrated.values()), reverse=True):
            if len(slots) >= 3:
                break
            tied = [f for f in dictionary.factors_names if calibrated[f] == cal_val and f not in used]
            if not tied:
                continue
            if len(tied) > 2:
                tied = random.sample(tied, 2)
                alert = True
            slots.append(tied)
            used.update(tied)
        letters = '-'.join(','.join(slot) for slot in slots)
        letters_abbr = '-'.join(','.join(dictionary.factors_abbr[f] for f in slot) for slot in slots)
        score.set('code', {'letters': letters, 'letters_abbr': letters_abbr, 'alert': alert})