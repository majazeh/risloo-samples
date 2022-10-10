from Data import Data
import scoring.dictionary.LMIQ93 as dictionary

class LMIQ93(Data):
    scores = {'raw' :  None }# 
    option_numbers = 5
    
    def scoring_raw(self, score):
        
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                score.increase('raw', self.option_numbers +1 - answer )
                for factor in factors:        
                    score.increase(factor , self.option_numbers +1 - answer )    
                
           
            except:
                pass
        
        self.calculate_converted_scores(score)
        

    def calculate_converted_scores(self,score):

        score.set('normalized_honesty', score.get('honesty')//4)
        score.set('normalized_responsibility', score.get('responsibility')//3)
        score.set('normalized_forgiveness', score.get('forgiveness')//2)
        score.set('normalized_emphaty', score.get('emphaty'))
            
        
        