from Data import Data
import scoring.dictionary.YBOCS93 as dictionary

class YBOCS93(Data):
    scores = {'raw' :  None }
    
    def scoring_raw(self, score):
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factor = dictionary.factors[i + 1]
                if (i >= 58 and i <= 62 and int(dict(self.items()).get(58).get('user_answered')) == 1) :
                    answer = 1
                score.increase(factor, answer if (i <58) else answer -1)
            except:
                pass

        find_level = None
        for level in dictionary.obsession_severity:
            if(score.get('obsession_severity') >= level):
                find_level = dictionary.obsession_severity.get(level)
                break
        score.set('obsession_severity_level', find_level.get('level'))
        score.set('report', find_level.get('title'))