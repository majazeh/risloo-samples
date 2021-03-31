from Data import Data
import scoring.dictionary.YTSI as dictionary

class YTSI(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    score.increase(factor , answer ) if factor else None
            except:
                pass
        
     