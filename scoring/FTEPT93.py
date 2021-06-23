from Data import Data
import scoring.dictionary.FTEPT93 as dictionary

class FTEPT93(Data):
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
                        score.increase('raw', option_numbers +1  - answer )
                        
                        score.increase(factor , option_numbers +1  - answer )    
                else :
                    for factor in factors:
                        
                        score.increase('raw', answer )
                        
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
        
     