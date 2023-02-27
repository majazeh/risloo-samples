from Data import Data
import scoring.dictionary.JLHSQ93 as dictionary

class JLHSQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i in dictionary.factorList:
            score.set(i,0)
            
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered'))  - 1
                try:
                    if(dictionary.reverse.index(i+1) >= 0):
                        answer = 2 - answer
                except:
                    pass
                factor = dictionary.factors[i + 1]
                score.increase('raw' , answer)
                score.increase(factor , answer )    
            except:
                pass
        
        