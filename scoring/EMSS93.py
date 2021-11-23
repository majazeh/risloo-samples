from Data import Data
import scoring.dictionary.EMSS93 as dictionary

class EMSS93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        score.set(dictionary.factors_names,0)
        option_numbers = dictionary.option_numbers
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
            
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    score.increase('raw' , option_numbers+1- answer )
                    
                    for factor in factors:
                        
                        score.increase(factor , option_numbers+1- answer )    
                else :
                    score.increase('raw' , answer )
                    
                    for factor in factors:
                        
                        score.increase(factor , answer )    
                

            except:
                
                pass
        
             
        raw_score = score.get('raw')
    
        t_score = self.raw2t_score(raw_score)
        score.set('t_score',t_score)
        
        summary = self.t_score_summary(t_score)
        score.set('t_score_summary',summary)

        # level2 report
        self.level2_report(score)
        
      
    def raw2t_score(self, raw_score ):
        
        intervals = list(dictionary.raw2t.keys())
        
        for interval in intervals:
            
            if interval[0] <= raw_score <= interval[1]:
                return dictionary.raw2t[interval]

        else:
            return None

    def t_score_summary(self, t_score):
        
        intervals = list(dictionary.t_score_summary.keys())
        
        for interval in intervals:
            
            if interval[0] <= t_score <= interval[1]:
                return dictionary.t_score_summary[interval]

        else:
            return None

    
    def level2_report(self, score):

        for f in list(dictionary.f_dic.keys()):
            test_factor = f
            test_factor_numbers = dictionary.f_dic[f]
            interpretation = self.scale_interpreting(score ,test_factor ,test_factor_numbers)
            score.set(test_factor + '_interpretation' , interpretation ) 


    def scale_interpreting(self,score ,test_factor ,test_factor_numbers):
        
        test_value = score.get(test_factor)
        test_normalized = round(test_value / test_factor_numbers)
        return dictionary.factors_interpretation[test_normalized]
        




     