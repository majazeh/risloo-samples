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
            if(i == 34 or i == 7):
                clinicalScore = 0 if answer <= 2 else 1
                answer = answer
            else:
                clinicalScore = 1 if answer <= 2 else 0
                answer = 5 - answer
                
            factors = dictionary.factors[i + 1]
            for factor in factors:
                groups['clinical'][factor]['raw'] += clinicalScore
                groups['clinical'][factor]['count'] += 1
                
                groups['research'][factor]['raw'] += answer - 1
                groups['research'][factor]['count'] += 3
            
        
        groups['clinical']['total']['raw'] += (21 - groups['clinical']['ambivalence']['raw']) + (17 - groups['clinical']['disobedience']['raw']) + groups['clinical']['adherence']['raw']
        groups['clinical']['total']['count'] = 60
        
        groups['research']['total']['raw'] += (63 - groups['research']['ambivalence']['raw']) + (51 - groups['research']['disobedience']['raw']) + groups['research']['adherence']['raw']
        groups['research']['total']['count'] = 180
        
        for group in groups:
            for factor in groups[group]:
                groups[group][factor]['percentage'] = round(groups[group][factor]['raw'] / groups[group][factor]['count'], 4)
                groups[group][factor].pop('count', None)
            score.set(group, groups[group])
            
        