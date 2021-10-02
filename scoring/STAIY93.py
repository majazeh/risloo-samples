from Data import Data
import scoring.dictionary.STAIY93 as dictionary

class STAIY93(Data):
    scores = {'state': 'state' , 'trait': 'trait'}# 
    
    def scoring_state(self, score):
        score.set('state',0)
        
        for i, item in self.items():   
            try:
                if i+1 > 20 :
                    break
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                if i+1 in dictionary.reverse_scoring_numbers:
                    for factor in factors:
                        score.increase(factor , dictionary.option_numbers + 1 - answer )    
                else :
                    for factor in factors:
                        score.increase(factor , answer )    
            except:
                pass
        
        state_score = score.get('state')
        interpretation_dict = dictionary.state_level_interpretation
        interpretation = self.get_level_interpretation(state_score ,
                                             interpretation_dict= interpretation_dict )
        score.set('interpretation', interpretation)

    
    def scoring_trait(self, score):
        score.set('trait',0)
        
        for i, item in self.items():   
            try:
                if i+1 <= 20 :
                    continue
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                if i+1 in dictionary.reverse_scoring_numbers:
                    for factor in factors:
                        score.increase(factor , dictionary.option_numbers + 1 - answer )    
                else :
                    for factor in factors:
                        score.increase(factor , answer )    
            except:
                pass
        
        state_score = score.get('trait')
        interpretation_dict = dictionary.trait_level_interpretation
        interpretation = self.get_level_interpretation(state_score ,
                                             interpretation_dict= interpretation_dict )
        score.set('interpretation', interpretation)

    
    def get_level_interpretation(self,raw_score , interpretation_dict = None):
        intervals = list(interpretation_dict.keys())
        
        for interval in intervals:    
            if interval[0] <= raw_score <= interval[1]:
                return interpretation_dict[interval]
        else:
            return None

        
        
        