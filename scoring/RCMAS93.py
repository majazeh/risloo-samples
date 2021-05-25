from Data import Data
import scoring.dictionary.RCMAS93 as dictionary

class RCMAS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        
        score.set(dictionary.factors_names,0)
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if answer == 1 :
                    my_score = 1 
                elif answer == 2:
                    my_score = 0 
    
                
                for factor in factors:
                    score.increase(factor , my_score ) 
                    
                    # all factors except f1 ='l'
                    if not factor == dictionary.f1:
                        score.increase('raw' , my_score ) 
                             
            except:
                pass
        

        
        