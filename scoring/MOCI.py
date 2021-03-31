from Data import Data
import scoring.dictionary.MOCI as dictionary

class MOCI(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors_dic = dictionary.factors[answer]
                
                
                if i + 1 in factors_dic.keys():
                    factors = factors_dic [i+1]
                    


                    for factor in factors:
                        score.increase(factor , weight = 1 )
            except:
                pass
        
     