from Data import Data
import scales.dictionary.DASS9A as dictionary
import scales.dictionary.DASS as g_dictionary

class DASS9A(Data):
    scores = {'raw':None , 'report':None }
 
    def scoring_raw(self, score):      
        score.set(g_dictionary.factors_name,0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                factor = dictionary.factors[i + 1]
                score.increase(factor , answer ) if factor else None
            except:
                pass
    
    def scoring_report(self, score):
        for factor in g_dictionary.factors_name:
            interval_dict = g_dictionary.factors_interval[factor]
            factor_value = score.get(factor)

            intensity = self.get_intensity(factor_value ,interval_dict)
            score.set(factor + '_intensity' , intensity)

    def get_intensity(self, factor_value ,interval_dict):
        intervals = list(interval_dict.keys())
        for interval in intervals:
            if len(interval) == 2:
                if interval[0] <= factor_value <= interval[1]:
                    return interval_dict[interval]

            else:
                return interval_dict[interval]