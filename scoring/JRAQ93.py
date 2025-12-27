from Data import Data
import scoring.dictionary.JRAQ93 as dictionary

groupList = ('clinical', 'research')

class JRAQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        groups = {}
        for group in groupList:
            groups[group] = {'total': {'raw': 0, 'count': 0}}
            for factor in dictionary.factors_names:
                groups[group][factor] = {'raw': 0, 'count': 0}
                
        for i, item in self.items():   
            answer = int(item.get('user_answered')) 
            if(i == 34):
                answer = 5 - answer
            factors = dictionary.factors[i + 1]
            clinicalScore = 0 if answer <= 2 else 1
            for factor in factors:
                groups['clinical'][factor]['raw'] += clinicalScore
                groups['clinical'][factor]['count'] += 1
                
                groups['research'][factor]['raw'] += answer - 1
                groups['research'][factor]['count'] += 3
                
        for i, item in self.items():   
            answer = int(item.get('user_answered'))
            answer = answer if 'adherence' in dictionary.factors[i +1] else (5 - answer)
            if(i == 34):
                answer = 5 - answer
            clinicalScore = 0 if answer <= 2 else 1
            groups['clinical']['total']['raw'] += clinicalScore
            groups['clinical']['total']['count'] += 1
            
            groups['research']['total']['raw'] += answer - 1
            groups['research']['total']['count'] += 3
        
        for group in groups:
            for factor in groups[group]:
                groups[group][factor]['percentage'] = round(groups[group][factor]['raw'] / groups[group][factor]['count'], 4)
                groups[group][factor].pop('count', None)
            score.set(group, groups[group])
            
        