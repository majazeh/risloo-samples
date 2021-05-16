f1 = 'frequency'
f2 = 'delay'
f3 = 'reading_breathing_and_word_pressure'
f4 = 'movement_of_limbs_and_body'
f5 = 'psychological_factors'
f6 = 'head_tongue_mouth_lips_movements'


factors_names = ('raw',f1,f2,f3,f4,f5,f6)
option_numbers = 5


factors = {
    1 :(f1,)
    , 2 :(f1,)
    , 3 :(f2,)
    , 4 :(f2,)
    , 5 :(f2,) 
    , 6 :(f2,)
    , 7:(f2,)
    , 8 :(f2,)
    , 9 :(f1,)
    , 10 :(f3,)
    , 11 :(f5,)
    , 12 :(f5,)
    , 13 :(f5,)
    , 14 :(f6,)
    , 15 :(f6,)
    , 16 :(f3,)
    , 17 :(f3,)
    , 18 :(f3,)
    , 19 :(f6,)
    , 20 :(f6,)
    , 21 :(f6,)
    , 22 :(f6,)
    , 23 :(f6,)
    , 24 :(f4,)
    , 25 :(f4,)
    , 26 :(f4,)
    , 27 :(f4,)
    , 28:(f4,)
    , 29 :(f5,)
    , 30 :(f5,)
    

}

level_interpretation = {
    (0,0): 'no_stuttering'
    ,(1,30): 'mild'
    ,(31,60) : 'moderate'
    ,(61,90) : 'severe'
    ,(91,120) : 'extreme'   
}
