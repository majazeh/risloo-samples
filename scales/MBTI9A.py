from Data import Data
import scales.dictionary.MBTI9A as dictionary

class MBTI9A(Data):
    scores = {'raw' :  None, 'report' : None}
    def scoring_raw(self, score):
        score.set(dictionary.factors_name, 0)
        for i, item in self.items():
            answer = int(item.get('user_answered'))
            factor = dictionary.factors[answer][i + 1]
            score.increase(factor) if factor else None
    
    def scoring_report(self, score):
        report = ''
        for group in dictionary.factors_group:
            report += self.find_biggest(group[0], group[1]) 
        score.set('report', report)
    
    def find_biggest(self, factor1, factor2):
        factor_value1 = self.score.get(factor1) if (self.score.get(factor1) != None) else 0
        factor_value2 = self.score.get(factor2) if (self.score.get(factor2) != None) else 0
        if(factor_value1 == factor_value2): return '(' + factor1 + factor2 + ')'
        elif (factor_value1 > factor_value2): return factor1
        return factor2
