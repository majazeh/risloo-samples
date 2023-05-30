from Data import Data
import scoring.dictionary.SPWB93 as dictionary

class SPWB93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                if i+1 in dictionary.reverse_scoring_numbers:
                    answer = 7 - answer
                
                factor = dictionary.items.get(i+1)
                score.increase('total' , answer )    
                score.increase(factor , answer )    

            except:
                pass
        
        