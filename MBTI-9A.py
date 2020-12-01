
from Inputs import Inputs,Scores
from Outputs import Outputs , Testdata




factors_dic = {
        1:{
            1:"I",5:"I",9:"I",13:"I",17:"I",21:"I",25:"I",29:"I",33:"I",37:"I",41:"I",45:"I",49:"I",53:"I",57:"I"
            , 2:"S", 6:"S", 10:"S", 14:"S", 18:"S", 22:"S", 26:"S",30:"S" ,34:"S",38:"S",42:"S",46:"S",50:"S",54:"S",58:"S"
            , 3:"T", 7:"T" , 11:"T", 15:"T", 19:"T",23:"T" ,27:"T", 31:"T" ,35:"T" ,39:"T",43:"T",47:"T",51:"T" ,55:"T",59:"T"
            , 4:"P", 8:"P", 12:"P", 16:"P", 20:"P", 24:"P", 28:"P", 32:"P", 36:"P", 40:"P", 44:"P", 48:"P", 52:"P", 56:"P", 60:"P" 
        }
            , 
        2 :{
            1:"E",5:"E",9:"E",13:"E",17:"E",21:"E",25:"E",29:"E",33:"E",37:"E",41:"E",45:"E",49:"E",53:"E",57:"E"
            , 2:"N", 6:"N", 10:"N", 14:"N", 18:"N", 22:"N", 26:"N",30:"N" ,34:"N",38:"N",42:"N",46:"N",50:"N",54:"N",58:"N"
            , 3:"F", 7:"F" , 11:"F", 15:"F", 19:"F",23:"F" ,27:"F", 31:"F" ,35:"F" ,39:"F",43:"F",47:"F",51:"F" ,55:"F",59:"F"
            , 4:"J", 8:"J", 12:"J", 16:"J", 20:"J", 24:"J", 28:"J", 32:"J", 36:"J", 40:"J", 44:"J", 48:"J", 52:"J", 56:"J", 60:"J" 
             
            }
        }
   
def get_factor(question_number,corresponded_choice,test_Scores):

    factor = factors_dic[corresponded_choice][question_number]  
    test_Scores.increase_score(factor , weight = 1 )

                
    return test_Scores        

def get_greater_factor(x='E',y='I'):

    if test_Scores.scores[x] > test_Scores.scores[y]:
        report = x
    
    elif test_Scores.scores[x] == test_Scores.scores[y]:
        report = '(' + x +',' + y +')'
    else :
        report = y
    
    return report







# Initiate the scores for this test
test_Scores = Scores()

# Add test factors for this special test
test_Scores.add_factor("E")
test_Scores.add_factor("I")
test_Scores.add_factor("S")
test_Scores.add_factor("N")
test_Scores.add_factor("T")
test_Scores.add_factor("F")
test_Scores.add_factor("J")
test_Scores.add_factor("P")


# Initiate the Inputs class for this test
my_input = Inputs()

# Get json data from Inputs class for this test
json_data = my_input.get_json_data()

# Scoring process
for i ,item in enumerate(json_data['items']):
    question_number = i+1
    corresponded_choice = item['user_answered']
    test_Scores = get_factor(int(question_number),int(corresponded_choice),test_Scores )


print(test_Scores.scores)

# get report of test
report = ''
result = get_greater_factor('E','I')
report = report + result

result = get_greater_factor('S','N')
report = report + result

result = get_greater_factor('T','F')
report = report + result

result = get_greater_factor('J','P')
report = report + result




# Give test outputs ,  to Outputs class
test_Outputs = Outputs(json_data , my_input)
output_json_data = test_Outputs.save_output(test_Scores ,report)
print(output_json_data)



