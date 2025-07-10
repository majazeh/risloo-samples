from Data import Data
import scoring.dictionary.PCL593 as dictionary

class PCL593(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'count': 0,
            }
        for factor in dictionary.dsm_factors:
            list[factor]['dsm_mode'] = 0

        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) - 1
                factors = dictionary.factors[i + 1]
                dsm = dictionary.dsm[i+1]
                
                if(answer >= 2):
                    list[dsm]['dsm_mode'] += 1
                    
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for factor in dictionary.factors_names:
            p = round(list[factor]['raw'] / (list[factor]['count'] * 4), 2)
            result = {"raw": list[factor]['raw'], "percentage": p}
            if('dsm_mode' in list[factor]):
                max = dictionary.dsm_factors[factor]
                result['dsm_mode'] = 'positive' if list[factor]['dsm_mode'] >= max else 'negative'
            score.set(factor, result)
        total = score.get('total')['raw']
        for level in dictionary.levels:
            if(total <= dictionary.levels[level]):
                score.set('status', level)
                break
    


        
        