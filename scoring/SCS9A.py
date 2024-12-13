from Data import Data

class SCS9A(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set('total' ,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                if i+1 in [1, 6, 8, 11]:
                    score.increase('total' , answer )
                else:
                    score.increase('total', 6 - answer)
            except:
                pass
        score.set('percentage' , score.get('total') / 65)
                
