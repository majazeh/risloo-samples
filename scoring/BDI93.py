from Data import Data
import scoring.dictionary.BDI93 as dictionary

class BDI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        suicide_alert = 0
        score.set(dictionary.factors_names,0)
        list = {}
        for factor in dictionary.factors_names:
            list[factor] = {
                'raw': 0,
                'percentage': 0,
                'count': 0
            }
        for i, item in self.items():   
            try:
                option = int(item.get('user_answered'))

                if(i == 15 or i == 17):
                    if option == 1:
                        answer = 0
                    elif option <= 3:
                        answer = 1
                    elif option <= 5:
                        answer = 2
                    else:
                        answer = 3
                else:
                    answer = option - 1
                factors = dictionary.factors[i + 1]
                print([i+1, option, answer])
                if((i == 1 or i == 8) and answer != 0):
                    suicide_alert+=1
                for factor in factors:
                    list[factor]['raw'] += answer
                    list[factor]['count'] += 1
            except:
                pass
        for factor in dictionary.factors_names:
            percentage = round(list[factor]['raw'] / (list[factor]['count'] * 3), 4)
            if factor == 'total':
                score.set('raw', list[factor]['raw'])
                score.set('percentage', percentage)
            else:
                score.set(factor, {
                    'raw': list[factor]['raw'],
                    'percentage': percentage
                })
        score.set('report', 'severe')
        score.set('suicide_alert', suicide_alert)
        for mark in dictionary.report:
            level = dictionary.report[mark]
            if score.get('raw') <= mark:
                score.set('report', level)
                break
    


        
        