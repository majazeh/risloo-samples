from Data import Data
import scoring.dictionary.BSCT93 as dictionary

class BSCT93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'percentage': 0,
                'count': 0
            }
        for i, item in self.items():
            try:
                if i+1 in dictionary.reverse_scoring_numbers:
                    answer = int(item.get('user_answered'))
                else:
                    answer = 6 - int(item.get('user_answered'))
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for factor in list:
            list[factor]['percentage'] = round(list[factor]['raw'] / (list[factor]['count'] * 5), 2)
            score.set(factor, {
                'raw': list[factor]['raw'],
                'percentage': list[factor]['percentage']
            })
                
    


        
        