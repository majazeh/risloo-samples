from Data import Data
import scoring.dictionary.TMPS93 as dictionary

class TMPS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        suicide_alert = 0
        score.set(dictionary.factors_names,0)
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'count': 0
            }
        for i, item in self.items():   
            try:
                option = int(item.get('user_answered'))
                answer = 6 - option
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for factor in dictionary.factors_names:
            percentage = round(list[factor]['raw'] / (list[factor]['count'] * 5), 4)
            score.set(factor, {
                'raw': list[factor]['raw'],
                'percentage': percentage
            })
    


        
        