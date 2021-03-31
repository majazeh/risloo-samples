f1 = 'DA'
f2 = 'HSE'
f3 = 'BP'
f4 = 'FR'
f5 = 'Ei'
f6 = 'AO'
f7 = 'PA'
f8 = 'D'
f9 = 'HC'
f10 = 'P'

option_numbers = 5

factor_names = (f1,f2,f3,f4,f5)

factors = {
    1 :(f1,)
    , 2 :(f2,)
    , 3 :(f3,)
    , 4 :(f4,)
    , 5 :(f5,) 
    , 6 :(f6,)
    , 7:(f7,)
    , 8 :(f8,)
    , 9 :(f9,)
    , 10 :(f10,)
    , 11 :(f1,)
    , 12 :(f2,)
    , 13 :(f3,)
    , 14 :(f4,)
    , 15 :(f5,)
    , 16 :(f6,)
    , 17 :(f7,)
    , 18 :(f8,)
    , 19 :(f9,)
    , 20 :(f10,)
    , 21 :(f1,)
    , 22 :(f2,)
    , 23 :(f3,)
    , 24 :(f4,)
    , 25 :(f5 ,)
    , 26 :(f6 ,)
    , 27 :(f7 ,)
    , 28:(f8,)
    , 29 :(f9,)
    , 30 :(f10,)
    , 31 :(f1,)
    , 32 :(f2 ,)
    , 33 :(f3,)
    , 34 : (f4,)
    , 35 :(f5,)
    , 36 :(f6,)
    , 37 :(f7,)
    , 38 :(f8,) 
    , 39 :(f9,)
    , 40:(f10,)
    , 41 :(f1,)
    , 42 :(f2,)
    , 43 :(f3,)
    , 44 :(f4,)
    , 45 :(f5,)
    , 46 :(f6,)
    , 47 :(f7,)
    , 48 :(f8,)
    , 49 :(f9,)
    , 50 :(f10,)
    , 51 :(f1,)
    , 52 :(f2,)
    , 53 :(f3,)
    , 54 :(f4,)
    , 55 :(f5,)
    , 56 :(f6,)
    , 57 :(f7,)
    , 58 :(f8 ,)
    , 59 :(f9 ,)
    , 60 :(f10 ,)
    , 61:(f1,)
    , 62 :(f2,)
    , 63 :(f3,)
    , 64 :(f4,)
    , 65 :(f5 ,)
    , 66 :(f6,)
    , 67 : (f7,)
    , 68 :(f8,)
    , 69 :(f9,)
    , 70 :(f10,) 
    , 71 :(f1,)
    , 72:(f2,)
    , 73 :(f3,)
    , 74 :(f4,)
    , 75 :(f5,)
    , 76 :(f6,)
    , 77 :(f7,)
    , 78 :(f8,)
    , 79 :(f9,)
    , 80 :(f10,)
    , 81 :(f1,)
    , 82 :(f2,)
    , 83 :(f3,)
    , 84 :(f4,)
    , 85 :(f5,)
    , 86 :(f6,)
    , 87 :(f7,)
    , 88 :(f8,)
    , 89 :(f9,)
    , 90 :(f10 ,)
    , 91 :(f1 ,)
    , 92 :(f2,)
    , 93:(f3,)
    , 94 :(f4,)
    , 95 :(f5,)
    , 96 :(f6,)
    , 97 :(f7 ,)
    , 98 :(f8,)
    , 99 : (f9,)
    , 100 : (f10,)
}


reverse_scoring_numbers =(4,5,11,14,15,16,17,22,25,29,30,31,32,35,36,37,39,40,41,43,44,45,48,52,54,56,57,58,59,60,61,63,64,65,68,70,77,80,83,85,86,87,88,91,98,93,94,95,97,98,99,100)

factors_interpretation = { (0,34) :'too_weak', (34,68):'weak' , (68,102):'intermediate' ,(102,1000):'strong' }