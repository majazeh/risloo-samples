import math
from Data import Data
import scoring.dictionary.MMFAD9A as dictionary

class MMFAD9A(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        lists = {}
        for factor in dictionary.factors_names:
            lists[factor] = {
                "raw" : 0,
                "avg" : 0,
                "report": ''
            }
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    scoreAnswer = (option_numbers + 1 - answer) if i+1 in dictionary.reverse_scoring_numbers else answer
                    lists[factor]['raw'] += scoreAnswer 
                    lists[factor]['avg'] += 1
            except:
                pass
        for factor in lists:
            avg = math.floor((lists[factor]['raw'] / lists[factor]['avg']) * 10) / 10
            lists[factor]['avg'] = int(avg) if avg == int(avg) else avg
            lists[factor]['report'] = 'healthy' if lists[factor]['avg'] < dictionary.CoP[factor] else 'unhealthy'
            score.set(factor, lists[factor])
        
        