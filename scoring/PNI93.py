from Data import Data
import scoring.dictionary.PNI93 as dictionary

class PNI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                score.increase('raw', answer)
                factor = dictionary.factors[i + 1]
                score.increase(factor, answer)
            except:
                pass
        
        