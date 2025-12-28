from Data import Data
import scoring.dictionary.YMQ93 as dictionary

class YMQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        factorList = {}
        for factor in dictionary.factors_names:
            factorList[factor] = {
                "raw": 0,
                "count": 0,
            }
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    factorList[factor]['raw'] += answer
                    factorList[factor]['count'] += 1
            except:
                pass
        for factor in factorList:
            score.set(factor, {
                'raw': factorList[factor].get('raw'),
                'mean': round(factorList[factor].get('raw') / factorList[factor].get('count'), 2),
            })
    
    
        
     