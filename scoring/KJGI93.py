from Data import Data
import scoring.dictionary.KJGI93 as dictionary

class KJGI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    score.increase('raw' , option_numbers +1  - answer )
                    for factor in factors:
                        
                        score.increase(factor , option_numbers +1  - answer )    
                else :
                    
                    score.increase('raw', answer )
                    for factor in factors:
                         
                        score.increase(factor , answer )    
                
           
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
        
        