from Data import Data
import scoring.dictionary.FACES93 as dictionary

class FACES93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names,0)
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]

                for factor in factors:
                    score.increase(factor , answer )    
            
            except:
                pass
        
        self.score_compound_factors(score)
        # self.score_weighted_factors(score)

        interpretation = self.get_interpretation_level(score)

        score.set('interpretation', interpretation)

    
    def score_compound_factors(self,score):
        
        a = score.get('a')
        f = score.get('f')
        e = score.get('e')

        score.set(dictionary.f9, a + (f-e)/2)

        b = score.get('b')
        d = score.get('d')
        c = score.get('c')

        score.set(dictionary.f10, b + (d-c)/2)


    def score_weighted_factors(self,score):
        
        a,b,c = score.get('a'), score.get('b') ,score.get('c')
        d,e,f = score.get('d'), score.get('e'), score.get('f')

        weight = 100 /35
        score.set('weighted_a', a*weight)
        score.set('weighted_b', b*weight)
        score.set('weighted_c', c*weight)
        score.set('weighted_d', d*weight)
        score.set('weighted_e', e*weight)
        score.set('weighted_f', f*weight)

        weight = 100 /50
        communication = score.get('communication')
        score.set('weighted_communication', communication*weight)
        
        weight = 100 /50
        satisfaction = score.get('satisfaction')
        score.set('weighted_satisfaction', satisfaction*weight)
        
        weight = 100 /5.52
        cohesion = score.get('cohesion')
        score.set('weighted_cohesion', cohesion*weight)

        weight = 100 /5.52
        flexibility = score.get('flexibility')
        score.set('weighted_flexibility', flexibility*weight)

    
    def get_interpretation_level(self,score):
        
        cohesion_percent, flexibility_percent = self.convert_scores_to_percentages(score)
        
        for condition in dictionary.interpretation_conditions:
            if self.check_condition(cohesion_percent, condition["cohesion_range"]) and self.check_condition(flexibility_percent ,condition["flexibility_range"]):
                    return condition["result"]
        
        return None

        
    def convert_scores_to_percentages(self,score):
         
        cohesion = score.get(dictionary.f9)
        flexibility = score.get(dictionary.f10)

        cohesion_percent = 100 * ((cohesion - dictionary.percentage_converter["min"])/(dictionary.percentage_converter["max"] - dictionary.percentage_converter["min"]))
        flexibility_percent = 100 * ((flexibility - dictionary.percentage_converter["min"])/(dictionary.percentage_converter["max"] - dictionary.percentage_converter["min"]))

        return cohesion_percent, flexibility_percent

    
    def check_condition(self,percent , condition):  
        
        if condition[0] <= percent <= condition[1]:
            return True
        else :
            return False
        
        