from Data import Data
import scales.dictionary.YBOCS_FATHI as dictionary

class YBOCS_FATHI(Data):
    scores = {'raw':None }
 
    def scoring_raw(self, score):      
      
        
        score.set(dictionary.factors_name,0)
        
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[i + 1]
                score.increase(factor , answer ) if factor else None
            except:
                pass
    
    


    
       
    
        
        

    