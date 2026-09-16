from Data import Data
import scoring.dictionary.ALVVCT93 as dictionary

class ALVVCT93(Data):
    scores = {'raw' :  None }# 
    
    MAXIMUM_SCORE = 70 
    
    def scoring_raw(self, score):
        
        self.all_items = list(self.items())
        
        score.set(dictionary.factors_names,0)
        option_numbers = dictionary.option_numbers
        
        list_factors = {}
        for factor in dictionary.factors_names:
            list_factors[factor] = {
                'raw' : 0,
                'percentage' : 0
            }
        for i, item in self.all_items[0:30]:   
            try:
                answer = int(item.get('user_answered')) 
                factors = dictionary.factors[i + 1]

                    
                list_factors[factors[0]]['raw'] += option_numbers - answer 
                
                list_factors[factors[1]]['raw'] += answer - 1    
            
           
            except:
                pass

        genderCheck = False
        for i, item in self.all_items[30:46] :   
            try:
                if(genderCheck == True and i == 44):
                    continue
                elif(genderCheck == False and i == 44 and item.get('user_answered') == None):
                    sorted_answer = [1,2,3,4]
                elif(i == 43 and item.get('user_answered') != None):
                    genderCheck = True
                sorted_answer = [int(x) for x in item.get('user_answered').split(",")]
                factors = dictionary.factors[i + 1]
                
                list_factors[factors[sorted_answer[0]-1]]['raw'] += 4
                list_factors[factors[sorted_answer[1]-1]]['raw'] += 3
                list_factors[factors[sorted_answer[2]-1]]['raw'] += 2
                list_factors[factors[sorted_answer[3]-1]]['raw'] += 1

            except:
                pass
        
        for factor in list_factors:
            list_factors[factor]['percentage'] = round(list_factors[factor]['raw']/self.MAXIMUM_SCORE, 3)
            score.set(factor, list_factors[factor])

        
        
            