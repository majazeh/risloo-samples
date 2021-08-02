from Data import Data
import scoring.dictionary.HDRS93 as dictionary

class HDRS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        
        option_numbers = dictionary.option_numbers
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                score.increase('raw' , answer-1 )

            except:
                pass
        
        