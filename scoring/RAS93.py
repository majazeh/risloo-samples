from Data import Data

class RAS93(Data):
    scores = {'raw' :  None }#
    
    def scoring_raw(self, score):
        score.set("raw",0)
        for i, item in self.items():   
            try:
                answer = 8 - int(item.get('user_answered')) 
                score.increase("raw" , answer )
            except:
                pass


        
     