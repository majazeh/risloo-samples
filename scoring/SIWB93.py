from Data import Data
import scoring.dictionary.SIWB93 as dictionary

class SIWB93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        iScore = {
            "self_efficacy" : {
                "score": 0,
                "percentage": 0,
            },
            'life_scheme' : {
                "score": 0,
                "percentage": 0,
            },
            'total' : {
                "score": 0,
                "percentage": 0,
            },
        }
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i + 1]
                iScore[factor]['score'] += answer
                iScore[factor]['percentage'] += 5
                iScore['total']['score'] += answer
                iScore['total']['percentage'] += 5
            except:
                pass
        for i in dictionary.factors_names:
            iScore[i]['percentage'] = round(iScore[i]['score']/iScore[i]['percentage'], 4)
            score.set(i, iScore[i])
            
        
     