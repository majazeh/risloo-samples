from Data import Data
import scoring.dictionary.SSS as dictionary

class SSS(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                score.increase('raw', answer-1 )
                for factor in factors:
                        
                    score.increase(factor , answer-1 )    
            
           
            except:
                pass
        
        raw_score = score.get('raw')
        interpretation = self.get_level_interpretation(raw_score)
        score.set('interpretation', interpretation)

    def get_level_interpretation(self,raw_score):
        
        intervals = list(dictionary.level_interpretation.keys())
        
        for interval in intervals:
            
            if interval[0] <= raw_score <= interval[1]:
                return dictionary.level_interpretation[interval]

        else:
            return None
        
        