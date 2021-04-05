from Data import Data
import scoring.dictionary.JRAQ as dictionary

class JRAQ(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):

        key_word_1 = 'first_scoring_'
        key_word_2 = 'second_scoring_'
        key_word_3 = 'raw_3_'
        
        option_numbers = dictionary.option_numbers


        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                for factor in factors:
                        
                        self.raw_1_scoring(factor = factor , question = i+1 , answer = answer ,score = score, key_word = key_word_1  )
                        self.raw_2_scoring(factor =factor , question = i+1 , answer = answer ,score = score, key_word = key_word_2 ) 
                        self.raw_3_scoring (factor ,answer ,score ,key_word_1 , key_word_2, key_word_3)                           
            except:
                pass

        
    
    
    def raw_1_scoring(self, factor , question ,answer ,score ,key_word  ):
        

        if answer ==1 or answer ==2 :
            sco = 0
        else :
            sco = 1

        if question in dictionary.reverse_scoring_numbers[factor]:
            
            score.increase(key_word + factor , 1 - sco ) 
        
        else:            
            score.increase(key_word + factor , sco ) 

         

    
    def raw_2_scoring(self, factor , question ,answer ,score ,key_word ):
        
        if question in dictionary.reverse_scoring_numbers[factor]:
            score.increase(key_word + factor , 4 - answer ) 
        
        else:            
            score.increase(key_word + factor , answer - 1 )
        
        
    

    def raw_3_scoring(self, factor  ,answer ,score ,key_word_1 , key_word_2, key_word_3):
        
        if factor == dictionary.f2 or factor == dictionary.f3 :
            
            # first scoring
            if answer == 1 or answer == 2 :
                sco = 1
            else :
                sco = 0

            # reverse-scoring
            score.increase(key_word_3 + key_word_1 ,sco )
            
            # second scoring
            # reverse-scoring
            score.increase(key_word_3 + key_word_2 , 4 - answer)
            
            
        
        else :
            
            # first scoring
            if answer == 1 or answer == 2 :
                sco = 0
            else :
                sco = 1

            # direct-scoring
            score.increase(key_word_3 + key_word_1 ,sco )
            
            # second scoring
            # direct-scoring
            score.increase(key_word_3 + key_word_2 , answer - 1)
        

            
        
    