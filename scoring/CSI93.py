from Data import Data
import scoring.dictionary.CSI93 as dictionary

class CSI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if i + 1 in dictionary.exception_questions:
                    if answer == 1  :
                        value = 0
                    else:
                        value = 1
                elif i + 1 in dictionary.yes_no_questions :
                    if answer == 1 :
                        value = 1
                    else:
                        value = 0
                else:
                    if answer == 1  or answer == 2 :
                        value = 0
                    else:
                        value = 1

                for factor in factors:
                    score.increase(factor , value )
            except:
                pass
        
     