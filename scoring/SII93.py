from Data import Data
import scoring.dictionary.SII93 as dictionary

class SII93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        score.set(dictionary.factors_names, 0)
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'count': 0
            }
        for i, item in self.items():
            try:
                option = int(item.get('user_answered'))
                answer = 3 - option  # 1->2, 2->1, 3->0, 4->-1, 5->-2
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for factor in dictionary.factors_names:
            raw = list[factor]['raw']
            count = list[factor]['count']
            percentage = round((raw + count * 2) / (count * 4), 4)
            score.set(factor, {
                'raw': raw,
                'percentage': percentage
            })