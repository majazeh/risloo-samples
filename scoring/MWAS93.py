from Data import Data
import scoring.dictionary.MWAS93 as dictionary

class MWAS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set('total' ,0)
        score.set('percentage' ,0)
        factorItemTotal = {}
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered'))
                if i+1 not in dictionary.reversed_scoring_numbers:
                    answer = 6 - answer
                factors = dictionary.factors[i + 1]     
                score.increase('total', answer )
                for factor in factors:
                    if factor not in factorItemTotal:
                        factorItemTotal[factor] = {'percentage': 0, 'total': 0}
                    factorItemTotal[factor]['percentage'] += 5
                    factorItemTotal[factor]['total'] += answer
            except:
                pass
        for factor in factorItemTotal:
            factorItemTotal[factor]['percentage'] = factorItemTotal[factor]['total'] / factorItemTotal[factor]['percentage']
            score.set(factor, factorItemTotal[factor])
        score.set('percentage' , score.get('total') / 180)
