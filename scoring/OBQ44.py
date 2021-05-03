from Data import Data
import scoring.dictionary.OBQ44 as dictionary

class OBQ44(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        option_numbers = dictionary.option_numbers
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                score.increase('raw' , answer-4 )
                for factor in factors:
                        
                    score.increase(factor , answer-4 )    
            
           
            except:
                pass
        
        