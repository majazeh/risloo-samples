from Data import Data
import scoring.dictionary.Raven93 as dictionary

class Raven93(Data):
    scores = {'raw' :  None, 'iq' : None, 'percentile' : None, 'level' : None}
    def scoring_raw(self, score):
        score.set(dictionary.factors_names, 0)
        for i, item in self.items():
            if(item.get('user_answered') == None): continue
            factor = dictionary.factors[i + 1] == item.get('user_answered')
            score.increase('raw') if factor else None
    
    def scoring_iq(self, score):
            age = int(self.prerequisite('age', 'user_answered'))
            if age < 9: age = 9
            elif age > 18: age = 18
            
            iq = None
            raw = int(self.score.get('raw'))
            if(dictionary.iq[age].get(raw)):
                iq = dictionary.iq[age].get(raw)
            score.set('iq', iq)
    
    def scoring_percentile(self, score):
        iq = self.getIntIQ()
        score.set('percentile', dictionary.percentile[iq])

    def getIntIQ(self):
        iq = self.score.get('iq')
        if self.score.get('iq') == '>149':
            iq = 149
        elif self.score.get('iq') == '<51':
            iq = 57
        return iq
    def scoring_level(self, score):
        iq = self.getIntIQ()
        level = None
        for iq_level in dictionary.level:
            if(iq >= iq_level):
                level = dictionary.level.get(iq_level)
                break
        score.set('level', level.get('level'))
        score.set('report', level.get('title'))    

            
