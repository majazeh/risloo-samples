from Data import Data
import scoring.dictionary.DSWLS93 as dictionary

class DSWLS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                score.increase('raw' , answer )    
            except:
                pass
        
        