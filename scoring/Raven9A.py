from Data import Data
import scoring.dictionary.Raven9A as dictionary

class Raven9A(Data):
    scores = {'raw' :  None, 'iq' : None, 'percentile' : None, 'report' : None}
    def scoring_raw(self, score):
        score.set(dictionary.factors_names, 0)
        for i, item in self.items():
            if(item.get('user_answered') == None): continue
            if(i <= 11):
                factor = dictionary.factors_paper1[i + 1] == item.get('user_answered')
                score.increase('pre') if factor else None
            if(i == 11 and score.get('pre') < 6):
                # score.set('report', 'No minimum number of corrects!' )
                break
            if(i >= 12):
                i2 = i - 11
                factor = dictionary.factors_paper2[i2] == item.get('user_answered')
                score.increase('raw') if factor else None
    
    def scoring_iq(self, score):
            age = float(self.prerequisite('age', 'user_answered'))
            if age < 12: age = 12
            elif age > 18: age = 18

            if(score.get('pre') < 6):
                score.set('raw', 5)
            iq = None
            if(self.score.get('raw') in dictionary.iq and dictionary.iq[self.score.get('raw')].get(age)):
                iq = dictionary.iq[self.score.get('raw')].get(age)
                score.set('iq', iq)
    
    def scoring_percentile(self, score):
        iq = self.score.get('iq')
        operator = ''
        if isinstance(iq, str):
            operator = iq[0:1]
            iq = int(iq[1:])
        iq = min(max(88, iq), 141)
        score.set('percentile', operator + str(dictionary.percentile[iq]))
    
    def scoring_report(self, score):
        iq = self.score.get('iq')
        operator = None
        if isinstance(iq, str):
            operator = iq[0:1]
            iq = int(iq[1:])
        for i in dictionary.level:
            if(iq >= i):
                break
        score.set('level', dictionary.level[i].get('level'))
        score.set('report', dictionary.level[i].get('title'))

            
