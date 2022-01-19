## first stage
f1 = 'problem_solving'
f2 = 'happiness'
f3 = 'independence'
f4 = 'stress_tolerance'
f5 = 'self_actualize'
f6 = 'emotional_self_awareness'
f7 = 'reality_testing'
f8 = 'interpersonal_relationship'
f9 = 'optimism'
f10 = 'self_regard'
f11 = 'impulse_control'
f12 = 'flexibility'
f13 = 'responsibility'
f14 = 'empathy'
f15 = 'assertiveness'

## second_stage
f16 = 'intrapersonal_skills'
f17 = 'interpersonal_skills'
f18 = 'adjustment'
f19 = 'general_mood'
f20 = 'stress_management'






factors_names = ('raw',f1,f2,f3,f4,f5,f6,f7,f8,f9 ,f10 ,f11 ,f12,f13 
                , f14, f15, f16, f17, f18, f19, f20)


option_numbers = 5

factors = {
    1 :(f1,f18)
    , 16 :(f1,f18)
    , 31 :(f1,f18)
    , 46 :(f1,f18)
    , 61 :(f1,f18)
    , 76 :(f1,f18) 
    
    , 2 :(f2,f19)
    , 17:(f2,f19)
    , 32 :(f2,f19)
    , 47 :(f2,f19)
    , 62 :(f2,f19)
    , 77 :(f2,f19)
    
    , 3 :(f3,f16)
    , 18 :(f3,f16)
    , 33 :(f3,f16)
    , 48 :(f3,f16)
    , 63 :(f3,f16)
    , 78 :(f3,f16)
    
    , 4 :(f4,f20)
    , 19 :(f4,f20)
    , 34 :(f4,f20)
    , 49 :(f4,f20)
    , 64 :(f4,f20)
    , 79 :(f4,f20)
    
    , 5 :(f5,f16)
    , 20 :(f5 ,f16)
    , 35 :(f5 ,f16)
    , 50 :(f5 ,f16)
    , 65:(f5,f16)
    , 80 :(f5,f16)
    
    , 6 :(f6,f16)
    , 21 :(f6,f16)
    , 36 :(f6,f16)
    , 51 :(f6,f16)
    , 66 :(f6,f16)
    , 81: (f6,f16)

    , 7 :(f7,f18)
    , 22 :(f7,f18)
    , 37 :(f7,f18)
    , 52 :(f7,f18)
    , 67 : (f7,f18)
    , 82: (f7,f18)

    , 8 :(f8,f17)
    , 23 :(f8,f17)
    , 38 :(f8,f17)
    , 53 :(f8,f17)
    , 68 : (f8,f17)
    , 83: (f8,f17)
        
    , 9 :(f9,f19)
    , 24 :(f9,f19)
    , 39 :(f9,f19)
    , 54 :(f9,f19)
    , 69 : (f9,f19)
    , 84: (f9,f19)

    , 10 :(f10,f16)
    , 25 :(f10,f16)
    , 40 :(f10,f16)
    , 55 :(f10,f16)
    , 70 : (f10,f16)
    , 85: (f10,f16)

    , 11 :(f11,f20)
    , 26 :(f11,f20)
    , 41 :(f11,f20)
    , 56 :(f11,f20)
    , 71 : (f11,f20)
    , 86: (f11,f20)

    , 12 :(f12,f18)
    , 27 :(f12,f18)
    , 42 :(f12,f18)
    , 57 :(f12,f18)
    , 72 : (f12,f18)
    , 87: (f12,f18)

    , 13 :(f13,f17)
    , 28 :(f13,f17)
    , 43 :(f13,f17)
    , 58 :(f13,f17)
    , 73 : (f13,f17)
    , 88: (f13,f17)

    , 14 :(f14,f17)
    , 29 :(f14,f17)
    , 44 :(f14,f17)
    , 59 :(f14,f17)
    , 74 : (f14,f17)
    , 89: (f14,f17)

    , 15 :(f15,f16)
    , 30 :(f15,f16)
    , 45 :(f15,f16)
    , 60 :(f15,f16)
    , 75 : (f15,f16)
    , 90: (f15,f16)


}
reverse_scoring_numbers = (2,11,12,15,17,18,19,20,21,22,26,27,33,34,35,36,37,40,41,45,48,50,52,56,58,61,63,64,67,71,72,75,77,78,79,80,81,82,84,86,87,90)