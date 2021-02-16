from Data import Data
import interpreting.dictionary._16PF as dictionary

class _16PF(Data):
    interprets = {'raw' :  None}
    
    def interpreting_raw(self,interpret):
        
        self.converted_HR_scores = ()
        self.converted_LR_scores = ()
       
        for factor in dictionary.factors:
            #value = self.score.get(factor)
        
            value = 6
            
            converted_score = self.get_converted_scores(factor, value , HR=True)
            if converted_score is not None:
                self.converted_HR_scores = self.converted_HR_scores + (converted_score,)
            
            converted_score = self.get_converted_scores(factor, value , HR=False)
            if converted_score is not None:
                self.converted_LR_scores = self.converted_LR_scores + (converted_score,)
        
        
        print(self.converted_HR_scores)
        print(self.converted_LR_scores)

        self.level_1_report(interpret)
        self.level_2_report(interpret)
        self.level_3_report(interpret)
        self.level_4_report(interpret)
        

         



    def level_1_report(self, interpret ): #, score must be added
        
        interpret.bind_header("Level 1" , level =1)
        

        validity = self.check_test_validity()
        interpret.bind_header(dictionary.level_1_factors[0] , level =2)
        interpret.bind(validity)
        
        stand = self.check_person_stand()
        interpret.bind_header(dictionary.level_1_factors[1] , level =2)
        interpret.bind(stand) # person_stand

    
    def level_2_report(self ,interpret ):

        interpret.bind_header("Level 2" , level =1)
        
        level_2_factors = dictionary.level_2_factors
        
        level_2_keys = dictionary.level_2_keys
        
        level_2_criteria_dic = dictionary.level_2_criteria
        
        for i in range(len(level_2_factors)): #interpret each of items in the main dictionary
            
            interpret.bind_header(level_2_factors [i] , level =2)

            for j in range(len(level_2_keys)):
            
                compatibility_level = self.check_factors_exist( level_2_criteria_dic [ level_2_factors[i]][level_2_keys[j]])
                
                if compatibility_level != '' :            
                    break
            
            interpret.bind(compatibility_level)       
        

    def level_3_report(self ,interpret ):
        
        interpret.bind_header("Level 3" , level =1)

        interpret.bind_header("First order" , level =2)

        ################################### first order interpreting #########################

        reliability_dict = dictionary.first_order_factors
        
        report_dict = dictionary.first_order_dict

        

        
        interpret.bind_header("High reliable" , level =3)

        for converted_score in self.converted_HR_scores:
            
            interpret.bind_header(converted_score , level =4)
            
            for sentence in  report_dict [converted_score]:

                interpret.add_bullet_text(sentence)



        
        interpret.bind_header("Low reliable" , level =3)

        for converted_score in self.converted_LR_scores:
            
            interpret.bind_header(converted_score , level =4)
            
            for sentence in  report_dict [converted_score]:

                interpret.add_bullet_text(sentence)
        


        ################################### second order interpreting #########################

        

    def level_4_report(self ,interpret ):

        interpret.bind_header("Level 4" , level =1)

        interpret.bind_header("High reliable" , level =2)

        self.get_combinational_report(interpret, self.converted_HR_scores)

        interpret.bind_header("Low reliable" , level =2)

        self.get_combinational_report(interpret, self.converted_LR_scores)


        

    def get_converted_scores(self , factor, value , HR= True):
        
        if HR:
            thr1 , thr2 = 7 , 3
        else:
            thr1 , thr2 = 6 , 4

        if value >= thr1 : # thr1 is considered as + with negligence and <= 8 is considered as + with certainness
            return '+' + factor
            
        elif value <= thr2 :# thr2 is considered as + with negligence and >=2  is considered as - with certainness
            return '-' + factor
        else :
            return None


    def check_test_validity(self):
        

        B_counter = 0
        
        for i, item in self.items():
            if(item.get('user_answered') == None): continue
            try:
                answer = int(item.get('user_answered'))
                if answer == 2 :
                    B_counter = B_counter + 1
                
            except:
                pass
        
        
         # scoring_assessment_factors[0] ='test_validity'
        
        test_dict = dictionary.level_1_criteria[dictionary.level_1_factors[0]]
        
        key_list =list(test_dict.keys())
        
        if key_list[0] <= B_counter <= key_list[1]:
            return test_dict[key_list[0]]
        
        elif key_list[1] <= B_counter <= key_list[2]:
            return test_dict[key_list[1]]
        
        else  :
            return test_dict[key_list[2]]
        


    def check_person_stand(self):
        
        # I assume that converted_score is in the dictionary by default and it is computed in the scoring process
        # and we don't need to compute it during interpreting process. I also assume that it is saved in a tuple format.
        test_dict = dictionary.level_1_criteria[ dictionary.level_1_factors[1]]
        # scoring_assessment_factors[1] ='person_stand'

        key_list =list(test_dict.keys())

        result = self.check_factors_exist(test_dict[key_list[0]])
        
        if result == '':
            result = self.check_factors_exist(test_dict[key_list[1]])
            
        return result
        
  

    def check_factors_exist(self,test_tuple): # tuple[0] = tuple of factors you need to check , tuple[1] = interpretation  
        
        Flag = True
        for converted_factor in test_tuple[0]:
            if converted_factor not in self.converted_HR_scores:
                Flag = False

        if Flag ==  True :
            return test_tuple[1]
        return ''


    def get_combinational_report(self,interpret, converted_scores) :

        report_dict = dictionary.second_order_dict

        for converted_score in converted_scores:

            interpret.bind_header(converted_score[1:]+ 'الگوهای ترکیبی ' , level =3)
            
            for dic in report_dict [converted_score[1:]]:

                counter = 0

                for factor in dic['factors']:
                    if factor in converted_scores:
                        counter = counter + 1

                

                if counter == len(dic['factors']):

                    interpret.add_bullet_text(dic['sentences'])



    
         



        
 
