f1 = 'efficacy'
f2 = 'emotional_effects'
f3 = 'planning'
f4 = 'lack_of_consequence_control'
f5 = 'motivation'


factors_names = ('raw',f1,f2,f3,f4,f5)

option_numbers = 5

factors = {
    29 :(f1,)
    , 30 :(f1,)
    , 31 :(f1,)
    , 32 :(f1,)
    , 33 :(f1,)
    , 34 :(f1,)
    , 35 :(f1,)
    , 36 :(f1,)
    
    , 12 :(f2,)
    , 13 :(f2,)
    , 14 :(f2,)
    , 15 :(f2,)
    , 16 :(f2,)
    , 17 :(f2,)
    , 18 :(f2,)
    , 19 :(f2,)
    
    , 1 :(f3,)
    , 2 :(f3,)
    , 3 :(f3,)
    , 4 :(f3,)
    , 8 :(f3,)
    , 9 :(f3,)
    , 10 :(f3,)
    , 11 :(f3,)
    , 40 :(f3 ,)
    , 43 :(f3 ,)
    , 44 :(f3 ,)
    , 45:(f3,)
    , 46 :(f3,)
    , 48 :(f3,)
    
    , 5 :(f4,)
    , 6 :(f4,)
    , 7 :(f4,)
    , 37 :(f4,)
    , 38 :(f4,)


    , 20 :(f5,)
    , 21 :(f5,)
    , 22 :(f5,)
    , 23 :(f5,)
    , 24 :(f5,)
    , 25 :(f5,)
    , 26 :(f5,)
    , 27 :(f5,)
    , 28 :(f5,)
    , 39 :(f5,)
    , 41 :(f5,)
    , 42 :(f5,)
    , 47 :(f5,)

}
reverse_scoring_numbers = (8,23,26,33)

level_interpretation = {
    (48,95): 'weak'
    ,(96,144): 'mild'
    ,(144,1000) : 'very_good'
}
