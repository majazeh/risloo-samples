from Data import Data
import scoring.dictionary.IBT93 as dictionary

class IBT93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers 
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    for factor in factors:
                        score.increase('raw', option_numbers+1- answer) 
                        score.increase(factor , option_numbers+1- answer )  
                         
                else :
                    for factor in factors:
                        score.increase('raw', answer)
                        score.increase(factor , answer )    
                        
                

            except:
                pass
        
        raw_value = score.get('raw')
        intervals = list(dictionary.factors_interpretation.keys())
        for interval in intervals:
           
            if interval[0]<= raw_value <=interval[1] :
                interpret = dictionary.factors_interpretation[interval]
                score.set('interpretation' , interpret)
                