from Data import Data
import scoring.dictionary.Raven9A as dictionary

class Raven9A(Data):
    scores = {'raw' :  None, 'iq' : None, 'percentile' : None, 'final' : None}
    def scoring_raw(self, score):
        score.set(dictionary.factors_name, 0)
        for i, item in self.items():
            if(item.get('user_answered') == None): continue
            if(i <= 11):
                factor = dictionary.factors_paper1[i + 1] == item.get('user_answered')
                score.increase('pre') if factor else None
            if(i == 11 and score.get('pre') < 6): break
            if(i >= 12):
                i2 = i - 11
                factor = dictionary.factors_paper2[i2] == item.get('user_answered')
                score.increase('raw') if factor else None
    
    def scoring_iq(self, score):
            age = int(self.prerequisite('age', 'user_answered'))
            if age < 6: age = 6
            elif age > 18: age = 18
            
            iq = 87
            if(self.score.get('raw') in dictionary.iq and dictionary.iq[self.score.get('raw')].get(age)):
                iq = dictionary.iq[self.score.get('raw')].get(age)
            score.set('iq', iq)
    
    def scoring_percentile(self, score):
        iq = min(max(87, self.score.get('iq')), 141)
        score.set('percentile', dictionary.percentile[iq])
    
    def scoring_level(self, score):
        raw_score = score.get('raw')
        intervals = list(dictionary.level_interpretation.keys())
        
        for interval in intervals:    
            if interval[0] <= raw_score <= interval[1]:
                score.set('report', dictionary.level_interpretation[interval])
                return 
        else:
            return None
        
        # for iq_level in dictionary.level:
        #     if(self.score.get('iq') >= iq_level):
        #         level = dictionary.level.get(iq_level)
        #         break
        # score.set('level', level.get('level'))
        # score.set('report', level.get('title'))

    def scoring_final(self, score):
        iq = score.get('iq')
        if(score.get('iq') == 87): iq = '<88'
        elif(score.get('iq') > 154): iq = '>154'

        score.set('iq', iq)
    

            
