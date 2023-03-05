from Data import Data
import scoring.dictionary.FMPS93 as dictionary

class FMPS93(Data):
    scores = {'raw' :  None }#
    
    def scoring_raw(self, score):
        score.set("raw",0)
        for factor in dictionary.factors_names:
            score.set(factor,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i+1]
                if(factor != 'organization'):
                    score.increase("raw" , answer )
                score.increase(factor, answer)
            except:
                pass
        score.set(dictionary.f7, score.get(dictionary.f5) + score.get(dictionary.f6))
        score.set(dictionary.f8, score.get(dictionary.f1) + score.get(dictionary.f2) + score.get(dictionary.f3) + score.get(dictionary.f4))
        


        
     