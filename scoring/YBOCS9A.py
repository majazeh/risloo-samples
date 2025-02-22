from Data import Data
import scoring.dictionary.YBOCS93 as dictionary

class YBOCS9A(Data):
    scores = {'raw' :  None }
    
    def scoring_raw(self, score):
        score.set('obsession_severity',0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                if (i >= 0 and i <= 4 and int(dict(self.items()).get(0).get('user_answered')) == 1) :
                    answer = 1
                if (i >= 5 and i <= 9 and int(dict(self.items()).get(5).get('user_answered')) == 1) :
                    answer = 1
                if(i < 12):
                    score.increase('obsession_severity', answer -1)
            except:
                pass

        find_level = None
        for level in dictionary.obsession_severity:
            if(score.get('obsession_severity') >= level):
                find_level = dictionary.obsession_severity.get(level)
                break
        score.set('obsession_severity_level', find_level.get('level'))
        score.set('report', find_level.get('title'))