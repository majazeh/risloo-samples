f1 = 'listening'
f2 = 'emotion_regulation'
f3 = 'understanding_message'
f4 = 'awareness'
f5 = 'assertiveness'

factor_names = (f1,f2,f3,f4,f5)
option_numbers = 5
factors = {
    1 :(f5,)
    , 2 :(f3,)
    , 3 :(f5,)
    , 4 :(f2,)
    , 5 :(f1,) 
    , 6 :(f1,)
    , 7:(f1,)
    , 8 :(f1,)
    , 9 :(f2,)
    , 10 :(f5,)
    , 11 :(f3,)
    , 12 :(f3,)
    , 13 :(f3,)
    , 14 :(f3,)
    , 15 :(f2,)
    , 16 :(f4,)
    , 17 :(f2,)
    , 18 :(f3,)
    , 19 :(f3,)
    , 20 :(f2,)
    , 21 :(f3,)
    , 22 :(f1,)
    , 23 :(f1,)
    , 24 :(f4,)
    , 25 :(f4 ,)
    , 26 :(f2 ,)
    , 27 :(f1 ,)
    , 28:(f3,)
    , 29 :(f4,)
    , 30 :(f2,)
    , 31 :(f2,)
    , 32 :(f5 ,)
    , 33 :(f5,)
    , 34 : (f4,)

}


reverse_scoring_numbers =(2,4,6,9,10,12,13,17,19,24,25,28,32,33)

factors_interpretation = { (0,34) :'بسیار ضعیف'
                        , (34,68):'ضعیف'
                        , (68,102):'متوسط'
                        ,(102,1000):'قوی' }