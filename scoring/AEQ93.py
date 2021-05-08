from Data import Data
import scoring.dictionary.AEQ93 as dictionary

class AEQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                        
                    score.increase('raw' , option_numbers +1  - answer )    
                
                else :
                        
                    score.increase('raw' , answer )    
                

            except:
                pass
        
        