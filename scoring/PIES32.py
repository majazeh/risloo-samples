from Data import Data
import scoring.dictionary.PIES32 as dictionary

class PIES32(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = 5
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    for factor in factors:
                        
                        score.increase(factor , option_numbers +1  - answer )    
                else :
                    for factor in factors:
                        
                        score.increase(factor , answer )    
                

            except:
                pass
        
        