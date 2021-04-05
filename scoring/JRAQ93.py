from Data import Data
import scoring.dictionary.JRAQ93 as dictionary

class JRAQ93(Data):
    scores = {'clinical':'clinical'  , 'researchical':'researchical' ,'raw' :None   }# 
    
    def scoring_raw(self, score):

       
        option_numbers = dictionary.option_numbers


        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                for factor in factors:
                         
                        self.third_scoring (factor ,answer ,score )                           
            except:
                pass

        
    
    def scoring_clinical(self,score):
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                for factor in factors:
                        
                        self.first_scoring(factor = factor , question = i+1 , answer = answer ,score = score )                           
            except:
                pass

    def scoring_researchical(self,score):
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                for factor in factors:
                        
                        self.second_scoring(factor =factor , question = i+1 , answer = answer ,score = score ) 
                           
            except:
                pass

    def first_scoring(self, factor , question ,answer ,score  ):
        

        if answer ==1 or answer ==2 :
            sco = 0
        else :
            sco = 1

        if question in dictionary.reverse_scoring_numbers[factor]:
            
            score.increase(factor , 1 - sco ) 
        
        else:            
            score.increase(factor , sco ) 

         

    
    def second_scoring(self, factor , question ,answer ,score ):
        
        if question in dictionary.reverse_scoring_numbers[factor]:
            score.increase(factor , 4 - answer ) 
        
        else:            
            score.increase(factor , answer - 1 )
        
        
    

    def third_scoring(self, factor  ,answer ,score ):
        
        if factor == dictionary.f2 or factor == dictionary.f3 :
            
            # first scoring
            if answer == 1 or answer == 2 :
                sco = 1
            else :
                sco = 0

            # reverse-scoring
            score.increase('clinical_raw' ,sco )
            
            # second scoring
            # reverse-scoring
            score.increase('researchical_raw' , 4 - answer)
            
            
        
        else :
            
            # first scoring
            if answer == 1 or answer == 2 :
                sco = 0
            else :
                sco = 1

            # direct-scoring
            score.increase('clinical_raw' ,sco )
            
            # second scoring
            # direct-scoring
            score.increase('researchical_raw' , answer - 1)
        

            
        
    