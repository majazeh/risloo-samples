f1 = 'conflicting_thoughts_of_self'
f2 = 'dichotomous_view_of_self'
f3 = 'fear_of_others_judgment'
f4 = 'preoccupation_with_self_worth'


option_numbers = 5

factors_names = ('raw',f1,f2,f3,f4)

factors = {
    4 :(f1,)
    , 7 :(f1,)
    , 8 :(f1,)
    , 11 :(f1,)
    , 12 :(f1,)
    , 16 :(f1,)
    , 17 :(f1,)
    

    , 3 :(f2,) 
    , 9 :(f2,)
    , 13 :(f2,)
    , 14 :(f2,)
    
    , 1 :(f3,)
    , 2 :(f3,)
    , 6 :(f3,)
    , 18 :(f3,)
    
    , 5 :(f4,)
    , 10 :(f4,)
    , 15 :(f4,)
    , 19 :(f4,)
    
    
}

level_interpretation = {
    (0,13):  ('very_desirable' , "0%-20%")
    ,(14,25): ('desirable' , "20%-40%")
    ,(26,37) : ('moderate' , "40%-60%")
    ,(38,49) : ('undesirable' , "60%-80%")
    ,(50,59) : ('very_undesirable' ,"80%-100%")
}
