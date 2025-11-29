f1 = 'cognitive'
f2 = 'affective'
f3 = 'somatic'
f4 = 'total'

factors_names = (f1,f2,f3,f4)
alert_items = (2, 9)
factors = {
    1 : (f2, f4),
    4 : (f2, f4),
    5 : (f2, f4),
    7 : (f2, f4),
    10 : (f2, f4),
    11 : (f2, f4),
    12 : (f2, f4),
    17 : (f2, f4),

    2: (f1, f4),
    3: (f1, f4),
    6: (f1, f4),
    8: (f1, f4),
    9: (f1, f4),
    13: (f1, f4),
    14: (f1, f4),
    19: (f1, f4),
    
    15: (f3, f4),
    16: (f3, f4),
    18: (f3, f4),
    20: (f3, f4),
    21: (f3, f4)
}

report = {
    13: 'minimal',
    19: 'mild',
    28: 'moderate',
    63: 'severe'
}