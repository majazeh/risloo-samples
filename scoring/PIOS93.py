from Data import Data
import scoring.dictionary.PIOS93 as dictionary

class PIOS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.f1, 0)
        score.set(dictionary.f2, 0)
        score.set(dictionary.f3, 0)
    
        for i, item in self.items():   
            try:             
                answer = int(item.get('user_answered')) 
                factor = dictionary.items[i + 1]
                score.increase(factor ,  answer - 1) 
                score.increase('total' ,  answer - 1) 
            except:
                pass
        
        