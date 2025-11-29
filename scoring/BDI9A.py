from Data import Data
import scoring.dictionary.BDI9A as dictionary

class BDI9A(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        suicide_alert = 0
        raw = 0
        for i, item in self.items():   
            try:
                answer = 4 - int(item.get('user_answered'))
                if((i == 1 or i == 6) and answer != 0):
                    suicide_alert+=1
                raw += answer
            except:
                pass
        
        score.set('raw', raw)
        score.set('percentage', round(raw / 39, 4))
        report = {
            'beck' : 'severe',
            'dadsetan' : 'severe',
        }
        score.set('suicide_alert', suicide_alert)
        for mark in dictionary.report_beck:
            level = dictionary.report_beck[mark]
            if raw <= mark:
                report['beck'] = level
                break
        
        for mark in dictionary.report_dadsetan:
            level = dictionary.report_dadsetan[mark]
            if raw <= mark:
                report['dadsetan'] = level
                break
        score.set('report', report)
    


        
        