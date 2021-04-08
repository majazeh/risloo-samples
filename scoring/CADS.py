from Data import Data
import scoring.dictionary.CADS as dictionary

class CADS(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                score.increase('raw' , answer-1 ) # 1 is mapped to 0              
            except:
                pass
        
     