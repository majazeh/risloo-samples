from Data import Data

class SEST93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                score.increase('total', answer -  1)
            except:
                pass
        score.set('percentage', round(score.get('total')/ 55, 4))
            
        
     