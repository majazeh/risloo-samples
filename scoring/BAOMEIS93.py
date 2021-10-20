from Data import Data
import scoring.dictionary.BAOMEIS93 as dictionary

class BAOMEIS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names, 0)
    
        score.set('raw' ,0)
        for i, item in self.items():   
            try:             
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                score.increase('raw' , option_numbers + 1 - answer )                         
                for factor in factors:    
                    score.increase(factor ,  option_numbers + 1 - answer) 

            except:
                pass
        
        