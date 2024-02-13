from Data import Data

class FMPQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                score.increase('total', answer)
            except:
                pass
        score.set('percentage', round(score.get('total')/ 52, 4))
            
        
     