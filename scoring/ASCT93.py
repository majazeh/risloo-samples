from Data import Data
import scoring.dictionary.ASCT93 as dictionary

class ASCT93(Data) :
    scores = {'raw' :  None }# 

    def scoring_raw(self, score):
        factors = {}
        for i in dictionary.factors_names:
            factors[i]= {'raw':0, 'percentage': 0, 'count': 0}
        for i, item in self.items():
            answer = int(item.get('user_answered')) - 1
            factor = dictionary.factors[i + 1]
            factors[factor]['raw'] += answer
            factors[factor]['count'] += 2
            factors['total']['raw'] += answer
            factors['total']['count'] += 2
        
        for i in factors:
            percentage = (factors[i]['raw'] * 100) / factors[i]['count']
            rp = round(percentage, 1) if round(percentage, 1) != round(percentage) else round(percentage)
            score.set(i, {
                'raw' : factors[i]['raw'],
                'percentage' : rp
            })