from Data import Data
import scoring.dictionary.SASQ93 as dictionary

class SASQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = dictionary.option_numbers 
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                
                score.increase('raw', answer)
 
            except:
                pass
        
        raw_value = score.get('raw')
        intervals = list(dictionary.factors_interpretation.keys())
        for interval in intervals:
           
            if interval[0]<= raw_value <=interval[1] :
                interpret = dictionary.factors_interpretation[interval]
                score.set('interpretation' , interpret)
                