from Data import Data
import scoring.dictionary.GJERQ93 as dictionary

class GJERQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i + 1]
                
                score.increase('total' , answer )
                score.increase(factor , answer )    
            
           
            except:
                pass
        
        