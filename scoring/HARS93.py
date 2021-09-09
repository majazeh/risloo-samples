from Data import Data
import scoring.dictionary.HARS93 as dictionary

class HARS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        
        option_numbers = dictionary.option_numbers
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                score.increase('raw' , answer-1 )

            except:
                pass
        
        raw_score = score.get('raw')
        interpretation = self._get_level_interpretation(raw_score)
        score.set('interpretation_level', interpretation)
        

    def _get_level_interpretation(self,raw_score):
        
        intervals = list(dictionary.level_interpretation.keys())
        
        for interval in intervals:
            if interval[0] <= raw_score <= interval[1]:
                return dictionary.level_interpretation[interval]

        else:
            return None
        
        