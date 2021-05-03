from Data import Data
import scoring.dictionary.JPSDI93 as dictionary

class JPSDI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i + 1][answer]
                
                score.increase(factor , 1 ) 
            except:
                pass
        
        
        # finding the maximun factor 
        factor_vals = []
        factors = []
        for factor in dictionary.factors_names:
            factors.append(factor)
            factor_vals.append(score.get(factor))
                
        
        maxims = [i for i in range(len(factor_vals)) if max(factor_vals) == factor_vals[i]] 
        
        

        string = []
        my_seperator = ','
        for i in range(len(maxims)) :
            string.append(factors[maxims[i]])
        score.set('psdi', my_seperator.join([str(elem) for elem in string]))