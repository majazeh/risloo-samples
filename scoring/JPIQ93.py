from Data import Data
import scoring.dictionary.JPIQ93 as dictionary

class JPIQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                if (i+1) in dictionary.reversed:
                    answer = int(item.get('user_answered')) - 1
                else:
                    answer = 5 - int(item.get('user_answered'))
                score.increase('penetrability_raw', answer)
            except:
                pass
        score.set('penetrability_percentage', round(score.get('penetrability_raw') / 56, 3))