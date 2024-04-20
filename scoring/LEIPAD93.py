from Data import Data
import scoring.dictionary.LEIPAD93 as dictionary

class LEIPAD93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names, 0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) - 1
                if i == 41:
                    if answer == 0 :
                        answer = 1
                    else :
                        answer = 0
                factor = dictionary.factors[i + 1]
                score.increase(factor , answer)
                if i < 32 :
                    score.increase('total_quality_of_life' , answer)
            except:
                pass
        
        