reverse_scoring_numbers = (1,2,3,5,7,9,10,17,25,26,27,28,29,33,34,36,44)
option_numbers = 5

raw2t = { 
    (73,77):12 , (78,82):14 ,   (83,87):16 , (88,92):18 ,  (93,97):19 , (98,102):21 , (103,107):23 ,(108,112):25 ,
    (113,117):27 , (118,122):29 ,   (123,127):31 , (128,132):33 ,  (133,137):35 , (138,142):36 , (143,147):38 ,(148,152):40 ,
    (153,157):42 , (158,162):44 ,   (163,167):46 , (168,172):48 ,  (173,177):50 , (178,182):52 , (183,187):53 ,(188,192):55 ,
    (193,197):57 , (198,202):59 ,   (203,207):61 , (208,212):63 ,  (213,217):65 , (218,222):67 , (223,227):69 ,(228,232):71 ,
    (233,237):72 
    
    }

t_score_summary = {
    (0,29) :'severe_dissatisfaction' ,
    (30,40) :'dissatisfaction' ,
    (41,60) :'moderate_satisfaction' ,
    (61,70) :'severe_satisfaction' ,
    (71,1000) :'extreme_satisfaction' 
}

f1 = 'personality_issues'
f2 = 'marital_communication'
f3 = 'Conflict_resolution'
f4 = 'financial_management'
f5 = 'leisure_activities'
f6 = 'sexual_relationship'
f7 = 'children_and_marriage'
f8 = 'family_and_friends'
f9 = 'religious_orientation'

factors_names = ('raw',f1,f2,f3,f4,f5,f6,f7,f8,f9)

f1_numbers = 6
f2_numbers = 6
f3_numbers = 5
f4_numbers = 5
f5_numbers = 5
f6_numbers = 5
f7_numbers = 5
f8_numbers = 5
f9_numbers = 5


f_dic = {f1 : f1_numbers ,f2 :f2_numbers ,f3 :f3_numbers ,f4 :f4_numbers ,
    f5: f5_numbers, f6:f6_numbers, f7:f7_numbers, f8:f8_numbers,f9:f9_numbers } 



factors = {
    1 :(f2,)
    , 2 :(f1,)
    , 3 :(f1,)
    , 4 :(f1,)
    , 5 :(f9,) 
    , 6 :(f2,)
    , 7:(f3,)
    , 8 :(f4,)
    , 9 :(f5,)
    , 10 :(f6,)
    , 11 :(f7,)
    , 12 :(f1,)
    , 13 :(f2,)
    , 14 :(f3,)
    , 15 :(f4,)
    , 16 :(f4,)
    , 17 :(f5,)
    , 18 :(f6,)
    , 19 :(f7,)
    , 20 :(f8,)
    , 21 :(f9,)
    , 22 :(f1,)
    , 23 :(f2,)
    , 24 :(f3,)
    , 25 :(f4 ,)
    , 26 :(f5 ,)
    , 27 :(f6 ,)
    , 28:(f7,)
    , 29 :(f8,)
    , 30 :(f9,)
    , 31 :(f8,)
    , 32 :(f2,)
    , 33 :(f3,)
    , 34 :(f4,)
    , 35 :(f5,)
    , 36 :(f6,)
    , 37 :(f7,)
    , 38 :(f8,)
    , 39 :(f9,)
    , 40 :(f1,)
    , 41 :(f2,)
    , 42 :(f3,)
    , 43 :(f5,)
    , 44 :(f6,)
    , 45 :(f7 ,)
    , 46 :(f8,)
    , 47:(f9,)

}

factors_interpretation = {
    1:'severe_dissatisfaction'
    , 2:'dissatisfaction'
    , 3:'moderate_satisfaction' 
    , 4:'severe_satisfaction' 
    , 5:'extreme_satisfaction'
}