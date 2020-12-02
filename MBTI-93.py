from Inputs import Inputs,Scores
from Outputs import Outputs , Testdata


factors_dic = {
            1 :{
                2: ("E" ,2) , 3: ("E" ,2) ,7: ("E" ,2) ,11: ("E" ,2) ,18: ("E" ,2) ,19: ("E" ,2) ,20: ("E" ,2) ,22: ("E" ,2) ,
                1:("E",1), 6:("E",1) , 21:("E",1) , 23:("E",1),  24:("E",1) , 25:("E",1) ,  
                15: ("E",0) , 
                12: ("I",2), 14: ("I",2), 20: ("I",2), 17: ("I",2),
                5: ("I",1), 8: ("I",1), 14: ("I",1), 16: ("I",1),
                4: ("I",0) , 9: ("I",0),
                26: ("S",2) , 28: ("S",2), 30: ("S",2) ,  32: ("S",2) , 33: ("S",2) , 34: ("S",2), 36: ("S",2) , 40: ("S",2),
                35 : ("S" , 1), 37 : ("S" , 1) ,38 : ("S" , 1) ,45 : ("S" , 1), 
                39 : ("S", 0) , 41 : ("S", 0),
                29 : ("N" , 2), 44 : ("N" , 2),
                27 : ("N" , 1), 31 : ("N" , 1), 42 : ("N" , 1), 43 : ("N" , 1), 46 : ("N" , 1), 47 : ("N" , 1), 49 : ("N" , 1),50 : ("N" , 1),
                48 : ("N",0), 
                54 : ("T",2), 57 : ("T",2), 59 : ("T",2), 61 : ("T",2), 65 : ("T",2), 71 : ("T",2), 74 : ("T",2),
                51 : ("T",1), 52 : ("T",1), 56 : ("T",1), 70 : ("T",1), 72 : ("T",1), 73 : ("T",1), 
                58 : ("T",0), 63 : ("T",0), 69 : ("T",0), 
                53 : ("F",2), 75 : ("F",2), 
                55 : ("F",1), 62 : ("F",1), 64 : ("F",1), 66 : ("F",1), 
                60 : ("F",0), 67 : ("F",0), 68 : ("F",0), 
                77 : ("J",2), 79 : ("J",2) , 81 : ("J",2), 82 : ("J",2) , 83 : ("J",2), 84 : ("J",2), 85 : ("J",2) 
                76 : ("J",1), 80 : ("J",1), 86 : ("J",1), 87 : ("J",1), 
                78 : ("P",1)
                }
    
                ,2:{
                    5:("E",2) , 12:("E",2) , 14:("E",2), 16:("E",2) , 17:("E",2),
                    4:("E",1), 9:("E",1), 13:("E",1), 
                    8:("E",0),
                    1:("I",2) , 2:("I",2) , 3:("I",2), 7:("I",2) , 11:("I",2), 19:("I",2) , 20:("I",2) , 23:("I",2), 24:("I",2),
                    6:("I",1) , 10:("I",2) , 15:("I",2), 18:("I",1) , 21:("I",1), 25:("I",1) ,
                    22:("I",0) , 
                    29:("S", 2), 31:("S", 2), 43:("S", 2), 44:("S", 2) , 46:("S", 2) , 
                    27:("S",1) ,47:("S",1) ,48:("S",1) ,
                    42:("S",0) ,49:("S",0) ,50:("S",0) ,
                    26:("N" , 2), 28:("N" , 2), 34:("N" , 2), 36:("N" , 2), 39:("N" , 2), 41:("N" , 2),
                    30:("N" , 1), 32:("N" , 1), 33:("N" , 1),35:("N" , 1), 37:("N" , 1), 38:("N" , 1), 40:("N" , 1),
                    45:("N" , 0),
                    53:("T" , 2), 62:("T" , 2), 66:("T" , 2), 67:("T" , 2), 68:("T" , 2), 75:("T" , 2),
                    55:("T" , 1), 6:("T" , 1), 64:("T" , 1),
                    54 : ("F",2), 57 : ("F",2), 58 : ("F",2), 63 : ("F",2), 65 : ("F",2), 69 : ("F",2), 71 : ("F",2), 72 : ("F",2), 73 : ("F",2), 74 : ("F",2), 
                    56 : ("F",1), 70 : ("F",1),
                    51 : ("F",0), 52 : ("F",0), 59 : ("F",0), 61 : ("F",0), 
                    78 : ("J" , 1),
                    76 : ("P",2), 77 : ("P",2), 80 : ("P",2), 83 : ("P",2), 84 : ("P",2), 85 : ("P",2), 87 : ("P",2), 
                    79 : ("P",1), 82 : ("P",1), 86 : ("P",1),
                    81 : ("P",0) 
                    
                }
                }
            
def get_factor(question_number,corresponded_choice,test_Scores):

    factor , weight = factors_dic[corresponded_choice][question_number]  
    test_Scores.increase_score(factor , weight = weight )

                
    return test_Scores 

def get_greater_factor(x='E',y='I'):

    if test_Scores.scores[x] > test_Scores.scores[y]:
        report = x
    
    elif test_Scores.scores[x] == test_Scores.scores[y]:
        report = '(' + x +',' + y +')'
    else :
        report = y
    
    return report

# Scoring process
for i ,item in enumerate(json_data['items']):
    question_number = i+1
    corresponded_choice = item['user_answered']
    test_Scores = get_factor(int(question_number),int(corresponded_choice),test_Scores )
       





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



