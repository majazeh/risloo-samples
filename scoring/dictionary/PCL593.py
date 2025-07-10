f1 = "intrusion"
f2 = "avoidance"
f3 = "negative_mood"
f4 = "arousal_reactivity"
f5 = "emotional_numbing"
f6 = "total"
f7 = "status"


factors_names = (f1,f2,f3, f4, f5, f6)
dsm_factors = {
    f1: 1,
    f2: 1,
    f3: 2,
    f4: 2
}

factors = {
    1: (f1, f6),
    2: (f1, f6),
    3: (f1, f6),
    4: (f1, f6),
    5: (f1, f6),

    6: (f2, f6),
    7: (f2, f6),
    
    8: (f3, f6),
    9: (f3, f6),
    10: (f3, f6),
    11: (f3, f6),

    16: (f4, f6),
    17: (f4, f6),
    18: (f4, f6),
    20: (f4, f6),
    
    12: (f5, f6),
    13: (f5, f6),
    14: (f5, f6),
    15: (f5, f6),
    19: (f5, f6)
}


dsm = {
    1: f1, 2: f1, 3: f1, 4: f1, 5: f1,

    6: f2, 7: f2,

    8: f3, 9: f3, 10: f3, 11: f3, 12: f3, 13: f3, 14: f3,

    15: f4, 16: f4, 17: f4, 18: f4, 19: f4, 20: f4

}
levels = {
    "minimal": 19,
    "mild": 27,
    "moderate":32 ,
    "severe": 80
}