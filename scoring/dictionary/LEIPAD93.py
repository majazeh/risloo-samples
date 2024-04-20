f1 = "physical_functioning"
f2 = "self_care"
f3 = "depression_anxiety"
f4 = "cognitive_functioning"
f5 = "social_functioning"
f6 = "sexual_functioning"
f7 = "life_satisfaction"
f8 = "total_quality_of_Life"
f9 = "the_perceived_personality_disorder"
f10 = "the_anger"
f11 = "the_social_desirability"
f12 = "self_esteem"
f13 = "trust_in_god"

factors_names = (f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13)


factors = {
    1: (f1,f8),
    6: (f1,f8),
    7: (f1,f8),
    9: (f1,f8),
    12: (f1,f8),

    2: (f2,f8),
    3: (f2,f8),
    4: (f2,f8),
    5: (f2,f8),
    10: (f2,f8),
    11: (f2,f8),

    17: (f3,f8),
    18: (f3,f8),
    19: (f3,f8),
    20: (f3,f8),

    8: (f4,f8),
    13: (f4,f8),
    14: (f4,f8),
    15: (f4,f8),
    16: (f4,f8),

    21: (f5,f8),
    22: (f5,f8),
    23: (f5,f8),

    24: (f6,f8),
    25: (f6,f8),

    26: (f7,f8),
    27: (f7,f8),
    28: (f7,f8),
    29: (f7,f8),
    30: (f7,f8),
    31: (f7,f8),

    39: (f9,),
    45: (f9,),
    46: (f9,),
    47: (f9,),
    48: (f9,),
    49: (f9,),

    32: (f10,),
    33: (f10,),
    34: (f10,),
    35: (f10,),

    42: (f11,),
    43: (f11,),
    44: (f11,),

    36: (f12),
    37: (f12,),
    38: (f12,),

    40: (f13,),
    41: (f13,),
}