from Data import Data
import scoring.dictionary.JSGS93 as dictionary

class JSGS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        list = {}
        for i in dictionary.factors_names:
            list[i]= {'raw':0, 'count': 0}
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 

                factors = dictionary.factors[i + 1]
                
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for i in list:
            score.set(i, {
                'raw' : list[i]['raw'],
                'percentage' : round(list[i]['raw'] / (list[i]['count'] * 4), 2)
            })
        
     