from Data import Data
import scoring.dictionary.JCSI93 as dictionary

class JCSI93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers
        score.set(dictionary.factors_names,0)
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
                
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    score.increase('raw', option_numbers+1- answer) 
                    for factor in factors:
                        
                        score.increase(factor , option_numbers +1- answer )  
                         
                else :
                    score.increase('raw', answer)
                    for factor in factors:
                        
                        score.increase(factor , answer )    
                        
                

            except:
                pass
        
        raw_value = score.get('raw')
        intervals = list(dictionary.factors_interpretation.keys())
        for interval in intervals:
           
            if interval[0]<= raw_value <=interval[1] :
                interpret = dictionary.factors_interpretation[interval]
                score.set('interpretation' , interpret)
                