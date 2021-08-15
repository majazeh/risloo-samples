f1 = 'general_self_steem'
f2 = 'family_self_steem'
f3 = 'social_self_steem'
f4 = 'professional_or_scholastic_self_steem'
f5 = 'life_scale'
f6 = 'total'

factors_names = (f1,f2,f3,f4,f5,f6)

factors = {
    1:{
        1 :(f1,f6)
        , 4 :(f1,f6,)
        , 19 :(f1,f6)
        , 27 :(f1,f6)
        , 38 :(f1,f6)
        , 39 :(f1,f6)
        , 43 :(f1,f6)
        , 47 :(f1,f6)
        
        , 9 :(f2,f6)
        , 20:(f2,f6)
        , 29 :(f2,f6)
        
        , 5 :(f3,f6)
        , 8 :(f3,f6)
        , 14 :(f3,f6)
        , 28 :(f3,f6)
        
        , 33:(f4,f6)
        , 37 :(f4,f6)
        , 52 :(f4,f6)

        , 26 :(f5,)
        , 32 :(f5,)
        , 36 :(f5,)
        , 41 :(f5,)
        , 45 :(f5,)
        , 50 :(f5,)
        , 53 :(f5,)
        , 58 :(f5,) 
    } ,
    2:{ 
        3 :(f1,f6)
        , 7 :(f1,f6) 
        , 10 :(f1,f6)
        , 12 :(f1,f6)
        , 13 :(f1,f6)
        , 15 :(f1,f6)
        , 18 :(f1,f6)
        , 24 :(f1,f6)
        , 25 :(f1,f6)
        , 30 :(f1,f6)
        , 31 :(f1,f6)
        , 32 :(f1,f6)
        , 35 :(f1,f6)
        , 48 :(f1,f6)
        , 51 :(f1 ,f6)
        , 55 :(f1 ,f6)
        , 56 :(f1,f6)
        , 57 :(f1,f6)

        , 6 :(f2 ,f6)
        , 11 :(f2 ,f6)
        , 16 :(f2,f6)
        , 22 :(f2,f6)
        , 44 :(f2,f6)

        , 21 :(f3 ,f6)
        , 40 :(f3 ,f6)
        , 49 :(f3,f6)
        , 52 :(f3,f6)
        
        , 2 :(f4 ,f6)
        , 17 :(f4 ,f6)
        , 23 :(f4,f6)
        , 46 :(f4,f6)
        , 54 :(f4,f6)

    }
}
level_interpretation = {
    (0,26):  ('mild')
    ,(27,43): ('moderate')
    ,(44,1000) : ('severe')
    }        
        
        




