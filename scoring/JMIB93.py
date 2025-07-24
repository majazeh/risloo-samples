from Data import Data
import scoring.dictionary.JMIB93 as dictionary

class JMIB93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'percentage': 0,
                'count': 0
            }
        for i, item in self.items():   
            try:
                answer = 5 - int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['count'] += 1
                    list[factor]['raw'] += answer
            except:
                pass
        for factor in dictionary.factors_names:
            list[factor]['percentage'] = round(list[factor]['raw'] / (list[factor]['count'] * 4), 3)
            score.set(factor, {'raw' : list[factor]['raw'], 'percentage' : list[factor]['percentage']})