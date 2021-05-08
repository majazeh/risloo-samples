from Data import Data
import scoring.dictionary.YSQ9093 as dictionary

class YSQ9093(Data):
    scores = {'raw':None}
 
    def scoring_raw(self, score): 
        score.set(dictionary.factors_name,0)
        
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                answer = None
                continue
            
            key = i + 1
            factor = dictionary.factors.get(key)
            score.increase(factor, answer)
            
            

                