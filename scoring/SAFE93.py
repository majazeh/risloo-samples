from Data import Data
import scoring.dictionary.SAFE93 as dictionary

class SAFE93(Data):
    scores = {'me_and_my_partner' : 'me_and_my_partner', 'me_and_my_children': 'me_and_my_children',
             'me_and_my_parents': 'me_and_my_parents' } 
    
    def scoring_me_and_my_partner(self, score):
        
        score.set(dictionary.factors_names,0)

        self.items = self.get_items_entirely()
        
        chosen_items = self.items[0:7]
        
        try:
        
            self.score_interaction(chosen_items,score)
            self.score_structure(chosen_items,score)
            
            interpretation = self.get_interpretation_level(score)

            score.set('interpretation', interpretation)
        except:
            pass 

    
    def scoring_me_and_my_children(self, score):
        
        score.set(dictionary.factors_names,0)
        
        chosen_items = self.items[7:14]
        
        try:
            self.score_interaction(chosen_items,score)
            self.score_structure(chosen_items,score)
            
            interpretation = self.get_interpretation_level(score)

            score.set('interpretation', interpretation)
        except:
            pass 

    def scoring_me_and_my_parents(self, score):
        
        score.set(dictionary.factors_names,0)
        
        chosen_items = self.items[14:]
        try:
            self.score_interaction(chosen_items,score)
            self.score_structure(chosen_items,score)

            interpretation = self.get_interpretation_level(score)

            score.set('interpretation', interpretation)
        except:
            pass 
        
    
    def score_interaction(self,items,score):

        for item in items[0:6]:  
            answer = int(item.get('user_answered'))

            if item["answer"]["reverse"]:  
                score.increase('interaction' , answer ) 
            
            else:
                score.increase('interaction' , answer ) 
            
    
    def score_structure(self,items,score):
            
        item = items[6]   
        answer = int(item.get('user_answered'))  
        
        if item["answer"]["reverse"]:     
            score.increase('structure' , (answer)*6 )
        
        else :
            score.increase('structure' , answer*6 )


    
    def get_interpretation_level(self,score):
            
        interaction = score.get(dictionary.f1)
        structure = score.get(dictionary.f2)

        for condition in dictionary.interpretation_conditions:
            if self.check_condition(interaction, condition["interaction_range"]) and self.check_condition(structure ,condition["structure_range"]):
                    return condition["result"]
        
        return None 
    
    
    def check_condition(self,raw , condition):  
        
        if condition[0] <= raw <= condition[1]:
            return True
        else :
            return False
        

        
        
