from Data import Data
import scoring.dictionary.BSSI93 as dictionary

class BSSI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'percentage': 0,
                'count': 0
            }
        for i, item in self.items():
            try:

                answer = int(item.get('user_answered')) - 1
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for factor in list:
            max_score = list[factor]['count'] * 2  # هر گویه حداکثر ۲ امتیاز دارد (گزینه۱=۰، گزینه۲=۱، گزینه۳=۲)
            list[factor]['percentage'] = round(list[factor]['raw'] / max_score, 2) if max_score else 0
            score.set(factor, {
                'raw': list[factor]['raw'],
                'percentage': list[factor]['percentage']
            })
                
    


        
        