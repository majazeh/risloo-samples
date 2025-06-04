from Data import Data
import scoring.dictionary.AAI93 as dictionary

class AAI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'percentage': 0,
            }
        for i, item in self.items():   
            try:
                answer = 6 - int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['raw'] += answer
            except:
                pass
        for factor in dictionary.factors_names:
            list[factor]['percentage'] = round(list[factor]['raw'] / 25, 2)
            score.set(factor, list[factor])
    


        
        