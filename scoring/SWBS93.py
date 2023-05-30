from Data import Data
import scoring.dictionary.SWBS93 as dictionary

class SWBS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                if i+1 in dictionary.reverse_scoring_numbers:
                    answer = 6 - answer
                
                score.increase('total' , answer )    

            except:
                pass
        
        