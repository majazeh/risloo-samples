from Data import Data

class IAT93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            answer = int(item.get('user_answered')) 
            score.increase('raw' , answer )            
        raw = score.get('raw')
        score.set('percentage', round(raw / 20, 4))
        score.set('report', 'severe_addiction')
        if(raw < 50):
            score.set('report', 'average_user')
        elif(raw < 80):
            score.set('report', 'moderate_addiction')
        
        