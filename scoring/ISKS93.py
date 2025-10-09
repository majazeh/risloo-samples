from Data import Data
import scoring.dictionary.ISKS93 as dictionary

class ISKS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():
            try:
                if i+1 in dictionary.reverse_scoring_numbers:
                    answer = 6 - int(item.get('user_answered'))
                else:
                    answer = int(item.get('user_answered'))
                raw += answer
            except:
                pass
        score.set('raw', raw)
        score.set('percentage', round(raw / 60, 2))
                
    


        
        