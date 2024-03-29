from Data import Data
import scoring.dictionary.Raven9Q as dictionary

class Raven9Q(Data):
    scores = {'raw' :  None , 'percentile_rank':'percentile_rank','iq' : 'iq'  }# 
    
    def scoring_raw(self, score):
        score.set('raw', 0)
        for i, item in self.items():
            if(item.get('user_answered') == None): continue
            answer = int(item.get('user_answered'))
            result = self.check_correctness(answer , i+1 )
            score.increase('raw') if result else None   
       
        # raw_score = score.get('raw')
        # interpretation = self.get_level_interpretation(raw_score)
        # score.set('report', interpretation)

    def get_level_interpretation(self,raw_score):
        
        intervals = list(dictionary.level_interpretation.keys())
        
        for interval in intervals:   
            if interval[0] <= raw_score <= interval[1]:
                return dictionary.level_interpretation[interval]
        else:
            return None
    
    
    def scoring_iq(self, score):      
        
        score.set(dictionary.factors_name_iq,0)
        self.grade_ravan_rahnema_iq(score)
        self.grade_irani_iq(score )
    
    def scoring_percentile_rank(self, score):

        score.set(dictionary.factors_name_percentile,0)
        raw_score = self.score.get('raw') 
        age = float(self.prerequisite('age').get('user_answered'))
        
        self.grade_ravan_rahnema_percentile(score , raw_score , age )
        self.grade_england_percentile(score , raw_score , age )
        self.grade_irani_percentile(score ,  raw_score , age)
    
    
    def check_correctness(self,answer = None , question = None) :
        if dictionary.correct_options[question] == answer:
            return True
        return False

    
    
    def grade_ravan_rahnema_iq(self, score ):
        
        percentile_rank = self.score.get('percentile_rank').get('ravan_rahnema')
        IQ_result = dictionary.IQ_ravan_rahnama[ percentile_rank ]
        score.set('ravan_rahnema' , IQ_result)

    
    
    def grade_irani_iq(self, score):

        raw_score = self.score.get('raw')
        age = float(self.prerequisite('age').get('user_answered'))
        

        irani_dict = dictionary.IQ_irani 
        age_list = list(irani_dict.keys())

        rounded_age = self.get_rounded_age(age , age_list)
        
        IQ_result = irani_dict[rounded_age][raw_score]
        score.set('irani' , IQ_result)


    def grade_irani_percentile(self, score ,  raw_score , age):

        irani_dict = dictionary.percentile_rank_irani
        
        age_list = list(irani_dict.keys())
        
        rounded_age = self.get_rounded_age(age , age_list)
        percentile_rank_result = self.get_percentile(rounded_age , raw_score , irani_dict)
        
        ###
        score.set('irani',percentile_rank_result)
        ###
    
    
    def grade_england_percentile(self, score ,  raw_score , age):

        england_dict = dictionary.percentile_rank_england
        
        age_list = list(england_dict.keys())
        

        rounded_age = self.get_rounded_age(age , age_list)
        
        percentile_rank_result = self.get_percentile(rounded_age , raw_score , england_dict)
        
        
        ###
        score.set('england',percentile_rank_result)
        ###
        
        

    def grade_ravan_rahnema_percentile(self, score ,raw_score , age):
        
        ravan_rahnama_dict = dictionary.percentile_rank_ravan_rahnama
        
        age_list = list(ravan_rahnama_dict.keys())
        
        rounded_age = self.get_rounded_age(age , age_list)
        
        percentile_rank_result = self.get_percentile(rounded_age , raw_score , ravan_rahnama_dict )
        
        ###
        score.set('ravan_rahnema',percentile_rank_result)
        ###
        
    

    def get_percentile(self , rounded_age , raw_score ,my_dictionary ) :
        
        numbers_list = list(my_dictionary[rounded_age].keys())
        
        if raw_score < numbers_list[0] : 
            percentile_rank_result = my_dictionary[rounded_age][numbers_list[0]] + '-'
            
        
        elif numbers_list[-1] <= raw_score  : 
            percentile_rank_result = my_dictionary[rounded_age][numbers_list[-1]] + '+'
            
        else :
            
            rounded_score = self.get_rounded_score(raw_score, numbers_list)
            percentile_rank_result = my_dictionary[rounded_age][rounded_score]

        return percentile_rank_result

    
    def get_rounded_age(self, age , age_list):
        
        N = len(age_list)
        if age <= age_list[0]:
            rounded_age = age_list[0]
            return rounded_age
        
        for i in range(N-2):  
            if age_list[i] <= age < age_list[i+1] :
                rounded_age = age_list[i]
                return rounded_age
        return age_list[N-1]

    def get_rounded_score(self ,raw_score, numbers_list):
                
        N = len(numbers_list)
        if raw_score <= numbers_list[0]:
            rounded_score = numbers_list[0]
            return rounded_score
        
        for i in range(N-2):
            if numbers_list[i] <= raw_score < numbers_list[i+1] : 
                rounded_score = numbers_list[i]
                
                return rounded_score
            
        
        return numbers_list[N-1]
        

