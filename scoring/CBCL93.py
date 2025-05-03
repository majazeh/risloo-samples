from Data import Data
import scoring.dictionary.CBCL93 as dictionary
import scoring.dictionary.CBCL93MC as mc
import scoring.dictionary.CBCL93MT as mt
import scoring.dictionary.CBCL93FC as fc
import scoring.dictionary.CBCL93FT as ft

class CBCL93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        gender = int(self.prerequisite('gender', 'user_answered')) if self.prerequisite('gender', 'user_answered') != None else None
        age = int(self.prerequisite('age', 'user_answered')) if self.prerequisite('age', 'user_answered') != None else None
        if(age > 18 or age < 6 or age == None):
            raise ValueError("age invalid")
        if(gender == None or (gender != 1 and gender != 2)):
            raise ValueError("gender notfound")
        factor_details = {}
        for f in dictionary.factors_names:
            if(f == dictionary.f9):
                continue
            factor_details[f] = {
                'pr': None,
                't': None,
                'value': 0,
                'status': None
            }
        score.set(dictionary.f9, 0)
        for i, item in self.items():
            if(i >= 119):
                continue
            try:
                answer = int(item.get('user_answered'))  -1
                factors = dictionary.factors[i + 1]
                for factor in factors:
                    if(factor == dictionary.f9):
                        score.increase(factor, answer ) if factor else None
                    else:
                        factor_details[factor]['value'] += answer
            except:
                pass
            
        boundle = 0
        for i, item in enumerate(self.get_items_entirely()[119:122]):
            try:
                answer = int(item.get('user_answered')) - 1
                boundle = answer if answer > boundle else boundle
            except:
                pass
        if(boundle > 0):
            score.increase(dictionary.f9, boundle)
            factor_details[dictionary.f12]['value'] += boundle
        pattern = ft
        if (gender == 2 and age <= 11):
            pattern = mc
        elif (gender == 2):
            pattern = mt
        elif gender == 1 and age <= 11:
            pattern = fc
        vars_list = [name for name in dir(pattern) if not name.startswith('__')]
        
        for f in vars_list:
            scores = getattr(pattern,f)
            factor = factor_details[f]
            value = factor['value']
            for score in scores:
                if(value >= score[0]):
                    factor_details[f]['pr'] = score[1]
                    factor_details[f]['t'] = score[2]
                    break
        for factor in factor_details:
            t = factor_details[factor]['t']
            if(factor in dictionary.group1):
                if(t >= 69):
                    factor_details[factor]['status'] = 'clinical'
                elif(t >= 64):
                    factor_details[factor]['status'] = 'borderline'
                else:
                    factor_details[factor]['status'] = 'normal'
            elif(factor in dictionary.group2):
                if(t >= 63):
                    factor_details[factor]['status'] = 'clinical'
                elif(t >= 59):
                    factor_details[factor]['status'] = 'borderline'
                else:
                    factor_details[factor]['status'] = 'normal'
        for factor in factor_details:
            self.score.set(factor, factor_details[factor])
        
    
        
     