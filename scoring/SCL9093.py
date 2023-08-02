from Data import Data
import scoring.dictionary.SCL9093 as dictionary

class SCL9093(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        factors = {}
        factors_total = {}
        score.set('total', 0)
        score.set('gsi', 0)
        score.set('pst', 0)
        score.set('psdi', 0)
        for i in dictionary.factors_names:
            factors[i] = {'raw':0, 'mean':0, 'report':'normal', 'status':0}
            factors_total[i] = 0
        
        for index, factor in list(dictionary.items.items()):
            factors_total[factor] += 1


        for i, item in self.items():   
            answer = int(item.get('user_answered')) - 1
            factor = dictionary.items[i+1]
            factors[factor]['raw'] += answer
            score.increase('total', answer)
            if(answer > 0):
                score.increase('pst')
        
        for index, value in list(factors.items()):
            factors[index]['mean'] = factors[index]['raw'] / factors_total[index]
            if(factors[index]['mean'] >=3):
                factors[index]['report'] = 'serious_clinical'
                factors[index]['status'] = 3
            elif(factors[index]['mean'] >=2.5):
                factors[index]['report'] = 'clinical'
                factors[index]['status'] = 2
            elif(factors[index]['mean'] >=1):
                factors[index]['report'] = 'abnormal'
                factors[index]['status'] = 1
            score.set(index, factors[index])

        score.set('gsi', score.get('total') / 90)
        score.set('psdi', score.get('total') / score.get('pst'))

        
        