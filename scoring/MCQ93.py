from Data import Data
import scoring.dictionary.MCQ93 as dictionary

class MCQ93(Data):
    scores = {'raw' :  None }# 
    def scoring_raw(self, score):
        _factors = {factor: {'total': 0, 'percentage': 0, "count": 0} for factor in dictionary.factors_names}
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    _factors[factor]['total'] += 6 - answer
                    _factors[factor]['count'] += 5
            except:
                pass
        for factor in _factors:
            if(_factors[factor]['total'] > 0):
                _factors[factor]['percentage'] = round(_factors[factor]['total'] / _factors[factor]['count'], 3)
            del _factors[factor]['count']
            score.set(factor, _factors[factor])

        
     