from Data import Data
import scoring.dictionary.CADS as dictionary

class CADS(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                if i+1 <= 12 :
                    score.increase('raw' , answer-1 ) # 1 is mapped to 0 

                else :
                    if answer == 1 :
                        score.increase('raw' , 1 )
                    else :
                        score.increase('raw' , 0 )
      
                             
            except:
                pass
        

        raw_score = score.get('raw')
        
        intervals = list(dictionary.factors_interpretation.keys())
        
        for interval in intervals:
            
            if interval[0] <= raw_score <= interval[1]:
                
                score.set('interpretation', dictionary.factors_interpretation[interval])

        
        