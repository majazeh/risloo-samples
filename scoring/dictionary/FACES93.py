f1 = 'a'
f2 = 'b'
f3 = 'c'
f4 = 'd'
f5 = 'e'
f6 = 'f'
f7 = 'communication'
f8 = 'satisfaction'
f9 = 'cohesion'
f10 = 'flexibility'


factors_names = (f1,f2,f3,f4,f5,f6,f7,f8,f9,f10)
option_numbers = 5


factors = {
    1 :(f1,)
    , 7 :(f1,)
    , 13 :(f1,)
    , 19 :(f1,)
    , 25 :(f1,)
    , 31 :(f1,)
    , 37 :(f1,)
    
    , 2 :(f2,)
    , 8 :(f2,)
    , 14 :(f2,) 
    , 20 :(f2,)
    , 26 :(f2,)
    , 32 :(f2,)
    , 38 :(f2,)
    
    , 3 :(f3,)
    , 9 :(f3,)
    , 15 :(f3,)
    , 21 :(f3,)
    , 27 :(f3,)
    , 33 :(f3,)
    , 39 :(f3,)
    
    , 4 :(f4,)
    , 10 :(f4,)
    , 16 :(f4,)
    , 22 :(f4,)
    , 28 :(f4,)
    , 34 :(f4,)
    , 40 :(f4,)
    
    , 5 :(f5,)
    , 11 :(f5,)
    , 17 :(f5,)
    , 23 :(f5,)
    , 29 :(f5,)
    , 35 :(f5,)
    , 41 :(f5,)
    
    , 6 :(f6,)
    , 12 :(f6,)
    , 18 :(f6,)
    , 24 :(f6,)
    , 30 :(f6,)
    , 36 :(f6,)
    , 42 :(f6,)
    
    , 43 :(f7,)
    , 44 :(f7,)
    , 45 :(f7,)
    , 46 :(f7,)
    , 47 :(f7,)
    , 48 :(f7,)
    , 49 :(f7,)
    , 50 :(f7,)
    , 51 :(f7,)
    , 52 :(f7,)
    
    , 53 :(f8,)
    , 54 :(f8,)
    , 55 :(f8,)
    , 56 :(f8,)
    , 57 :(f8,)
    , 58 :(f8,)
    , 59 :(f8,)
    , 60 :(f8,)
    , 61 :(f8,)
    , 62 :(f8,)
}

percentage_converter = {"min": -7 , "max":49}

interpretation_conditions = [
    { "cohesion_range" : (16,85), "flexibility_range" : (16,85), "result": 'balanced'},
    
    { "cohesion_range" : (16,85), "flexibility_range" : (0,15), "result": 'semi_balanced'},
    { "cohesion_range" : (16,85), "flexibility_range" : (86,100), "result": 'semi_balanced'},
    { "cohesion_range" : (0,15), "flexibility_range" : (16,85), "result": 'semi_balanced'},
    { "cohesion_range" : (86,100), "flexibility_range" : (16,85), "result": 'semi_balanced'},
    
    { "cohesion_range" : (86,100), "flexibility_range" : (86,100), "result": 'unbalanced'},
    { "cohesion_range" : (86,100), "flexibility_range" : (0,15), "result": 'unbalanced'},
    { "cohesion_range" : (0,15), "flexibility_range" : (86,100), "result": 'unbalanced'},
    { "cohesion_range" : (0,15), "flexibility_range" : (0,15), "result": 'unbalanced'}
]
