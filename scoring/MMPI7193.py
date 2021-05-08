from Data import Data
import scoring.dictionary.MMPI7193 as dictionary

class MMPI7193(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        
        t_dictionary = self.get_gender_and_education_dictionary()
        
        score.set(dictionary.factors_names,0)
        
        for i, item in self.items():   
            try:
                answer = int(item.get('user_answered')) 
                factors_dic = dictionary.factors[answer]
                
                
                if i + 1 in factors_dic.keys():
                    factors = factors_dic [i+1]
                    

                    for factor in factors:
                        score.increase(factor , weight = 1 )
            except:
                pass
        
        for factor in dictionary.factors_names:
            raw_factor_score = score.get(factor)
            t_factor_score = t_dictionary[factor][raw_factor_score]
            score.set(factor + "_t_score" ,t_factor_score)

    
    
    def get_gender_and_education_dictionary(self):
        
        prequesties = self.prerequisites()
        gender_label = int(prequesties["gender"]['user_answered'])
        education_label = int(prequesties["education"]['user_answered'])
          
        
        if gender_label == 1 :# Woman
            if education_label <= 5 :# student
                return dictionary.six_attachment
            else :
                return dictionary.seven_attachment #collegian
        elif gender_label == 2:# Man
            
            if education_label <= 5 :
                
                return dictionary.four_attachment# student
                
            else :
                return dictionary.five_attachment#collegian
        else :
            return None

            



     