f1 = 'attention_deficity_and_hyper_activity_disorder_type_a'
f2 = 'attention_deficity_and_hyper_activity_disorder_type_b'
f3 = 'attention_deficity_and_hyper_activity_disorder_total'
f4 = 'oppositional_defant_disorder'
f5 = 'conduct_disorder'
f6 = 'generalized_anxiety_disorder_type_a'
f7 = 'generalized_anxiety_disorder_type_b'
f8 = 'generalized_anxiety_disorder_type_c'
f9 = 'generalized_anxiety_disorder_total'
f10 = 'special_phobia'
f11 = 'obssesive'
f12 = 'compulsive'
f13 = 'post_terumatic_stress_disorder'
f14 = 'motor_tics'
f15 = 'vocal_tics'
f16 = 'schizophernia'
f17 = 'major_depression_type_a'
f18 = 'major_depression_type_b'
f19 = 'major_depression_total'
f20 = 'dysthymia_type_a'
f21 = 'dysthymia_type_b'
f22 = 'dysthymia_total'
f23 = 'autistic_disorder_type_a'
f24 = 'autistic_disorder_type_b'
f25 = 'autistic_disorder_type_c'
f26 = 'autistic_disorder_total'
f27 = 'asperger_disorder_type_a'
f28 = 'asperger_disorder_type_b'
f29 = 'asperger_disorder_total'
f30 = 'social_phobia'
f31 = 'seperation_anxiety_disorder'
f32 = 'enuresis'
f33 = 'encopresis'

factors_names = (f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,
                f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33)
factors = {
    1 :(f1,f3)
    , 2 :(f1,f3,f8,f9)
    , 3 :(f1,f3)
    , 4 :(f1,f3)
    , 5 :(f1,f3) 
    , 6 :(f1,f3)
    , 7:(f1,f3)
    , 8 :(f1,f3)
    , 9 :(f1,f3)
    , 10 :(f2,f3)
    , 11 :(f2,f3)
    , 12 :(f2,f3)
    , 13 :(f2,f3)
    , 14 :(f2,f3)
    , 15 :(f2,f3)
    , 16 :(f2,f3)
    , 17 :(f2,f3)
    , 18 :(f2,f3)
    , 19 :(f4,)
    , 20 :(f4,)
    , 21 :(f4,)
    , 22 :(f4,)
    , 23 :(f4,)
    , 24 :(f4,)
    , 25 :(f4,)
    , 26 :(f4,)
    , 27 :(f5,)
    , 28:(f5,)
    , 29 :(f5,)
    , 30 :(f5,)
    , 31 :(f5,)
    , 32 :(f5,)
    , 33 :(f5,)
    , 34 :(f5,)
    , 35 :(f5,)
    , 36 :(f5,)
    , 37 :(f5,)
    , 38 :(f5,)
    , 39 :(f5,)
    , 40 :(f5,)
    , 41 :(f5,)
    , 42 :(f6, f9)
    , 43 :(f7, f9)
    , 44 :(f8, f9)
    , 45 :(f8, f9, f17, f19 , f20 , f22)
    , 46 :(f8, f9)
    , 47 :(f10,)
    , 48 :(f11,)
    , 49 :(f12,)
    , 50 :(f13,)
    , 51 :(f14,)
    , 52 :(f15,)
    , 53 :(f16,)
    , 54 :(f16,)
    , 55 :(f16,)
    , 56 :(f16,)
    , 57 :(f16,)
    , 58 :(f17, f19 , f20 , f22)
    , 59 :(f17, f19)
    , 60 :(f18, f19)
    , 61 :(f18, f19)
    , 62 :(f8, f9, f18, f19 , f21, f22)
    , 63 :(f21, f22)
    , 64 :(f21, f22)
    , 65 :(f18, f19, f21, f22)
    , 66 :(f18, f19, f21, f22)
    , 67 :(f18, f19)
    , 68 :(f18, f19, f21, f22)
    , 69 :(f21, f22)
    , 70 :(f23, f26 , f27 ,f29)
    , 71 :(f23, f26, f27 ,f29)
    , 72 :(f23, f26, f27 ,f29)
    , 73 :(f23, f26, f27 ,f29)
    , 74 :(f24, f26)
    , 75 :(f24, f26)
    , 76 :(f24, f26)
    , 77 :(f24, f26)
    , 78 :(f25, f26, f28 ,f29)
    , 79 :(f25, f26, f28 ,f29)
    , 80 :(f25, f26, f28 ,f29)
    , 81 :(f25, f26, f28 ,f29)
    , 82 :(f30,)
    , 83 :(f30,)
    , 84 :(f30,)
    , 85 :(f30,)
    , 86 :(f31,)
    , 87 :(f31,)
    , 88 :(f31,)
    , 89 :(f31,)
    , 90 :(f31,)
    , 91 :(f31,)
    , 92 :(f31,)
    , 93 :(f31,)
    , 94 :(f32,)
    , 95 :(f33,) 
    , 96 :("96",)
    , 97 :("97",)
    , 98 :("98",)
    , 99 :("99",)
    , 100 :("100",)
    , 101 :("101",)
    , 102 :("102",)
    , 103 :("103",)
    , 104 :("104",)
    , 105 :("105",)
    , 106 :("106",)
    , 107 :("107",)
    , 108 :("108",)
    , 109 :("109",)
    , 110 :("110",)
}

exception_questions = (32,33,34,35,36,37,38,39,40,41,47,48,49,50,51,52,94,95)
yes_no_questions = (65,66,67,68,69)
extra_questions = (96,97,98,99,100,101,102,103,104,105,106,107,108,109,110)
