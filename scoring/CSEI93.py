from Data import Data
import scoring.dictionary.CSEI93 as dictionary

class CSEI93(Data):
    scores = {'raw' :  None , 'level':None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors_dic = dictionary.factors[answer]
                if i + 1 in factors_dic.keys():
                    factors = factors_dic [i+1]
                    for factor in factors:
                        score.increase(factor , weight = 1 )
            except:
                pass
        
    def scoring_level(self,score):
        raw_score = score.get('total')
        intervals = list(dictionary.level_interpretation.keys())
        for interval in intervals:    
            if interval[0] <= raw_score <= interval[1]:
                score.set('report', dictionary.level_interpretation[interval])
                return 
        else:
            return None


        
     