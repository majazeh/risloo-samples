from Data import Data
import scoring.dictionary.EMSS4793 as dictionary

class EMSS4793(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        option_numbers = 5
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    score.increase('raw' , option_numbers+1- answer ) 
                else :
                    score.increase('raw' , answer ) 

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
        
        flag = False
        for i in range(len(intervals)):
            if i == 0  :
                if  t_score <= intervals[i][0]:
                    return dictionary.t_score_summary[intervals[i]]
            
            elif i == len(intervals)-1:
                if  t_score >= intervals[i][0]:
                    return dictionary.t_score_summary[intervals[i]]
            else :
                if intervals[i][0] <= t_score <= intervals[i][1]:
                    return dictionary.t_score_summary[intervals[i]]
                return None
    
    def level2_report(self, score):
        option_numbers = dictionary.option_numbers 
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]
            
                if i+1 in dictionary.reverse_scoring_numbers:
                    
                    for factor in factors:
                        
                        score.increase(factor , option_numbers+1- answer )    
                else :
                    for factor in factors:
                        
                        score.increase(factor , answer )    
                

            except:
                pass
        
        for f in list(dictionary.f_dic.keys()):
            test_factor = f
            test_factor_numbers = dictionary.f_dic[f]
            self.scale_interpreting(score ,test_factor ,test_factor_numbers)


    def scale_interpreting(self,score ,test_factor ,test_factor_numbers):
        
        test_value = score.get(test_factor)
        test_normalized = round(test_value / test_factor_numbers)
        interpretation = dictionary.factors_interpretation[test_normalized]
        score.set(test_factor + '_interpretation' , interpretation ) 




     