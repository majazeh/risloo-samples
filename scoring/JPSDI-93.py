from Data import Data
import scoring.dictionary.JPSDI as dictionary

class JPSDI(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i + 1][answer]
                
                score.increase(factor , answer ) 
            except:
                pass
        
        maxim = 0 
        for factor in dictionary.factors_names:
            if score.get(factor) > maxim :
                max_factor , maxim = factor , score.get(factor)

        score.set('sath_tahavol_ravani_fard', max_factor)