from Data import Data
import scoring.dictionary.CRAAS93 as dictionary

class CRAAS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    for factor in factors:
                        
                        score.increase(factor , option_numbers  - answer )    
                else :
                    for factor in factors:
                        
                        score.increase(factor , answer -1  )    
                

            except:
                pass
        
        