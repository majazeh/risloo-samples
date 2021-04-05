from Data import Data
import scoring.dictionary.JPSDI93 as dictionary
import numpy as np

class JPSDI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i + 1][answer]
                
                score.increase(factor , answer ) 
            except:
                pass
        
        
        # finding the maximun factor 
        factor_vals = []
        factors = []
        for factor in dictionary.factors_names:
            factors.append(factor)
            factor_vals.append(score.get(factor))
                
        
        maxims = [i for i in range(len(factor_vals)) if max(factor_vals) == factor_vals[i]] 
        
        

        string = ''
        for i in range(len(maxims)) :
            string = string + factors[maxims[i]] + ','
        
        score.set('sath_tahavol_ravani_fard', string)