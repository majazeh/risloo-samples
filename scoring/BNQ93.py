from Data import Data
import scoring.dictionary.BNQ93 as dictionary

class BNQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'percentage': 0,
            }
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['raw'] += answer
            except:
                pass
            
        for factor in list:
            list[factor]['percentage'] = round(list[factor]['raw'] / 35, 2)
            score.set(factor, list[factor])
                
    


        
        