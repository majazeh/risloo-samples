factors = {
    1 :'Stress' , 2 :'Anxiety' , 3 :'Depression' , 4 :'Anxiety' , 5 :'Depression' , 6 :'Stress' ,  7:'Anxiety' , 8 :'Stress' , 9 :'Anxiety' , 10 :'Depression' , 11 :'Stress' , 12 :'Stress' , 13 :'Depression' , 14 :'Stress' , 15 :'Anxiety' , 16 :'Depression' ,
    17 :'Depression' , 18 :'Stress' , 19 :'Anxiety' , 20 :'Anxiety' , 21 :'Depression' 
}

factors_name = ('Stress' ,'Anxiety' , 'Depression')
factors_intensity = ('Stress_instensity' ,'Anxiety_instensity' , 'Depression_instensity')


factors_interval = { 
    'Depression': { (0,9):'Normal' , (10,13):'slight' , (14,20):'medium' ,(21,27): 'drastic',  (28,):'very_drastic' },
    'Anxiety': { (0,7):'Normal' , (8,9):'slight' , (10,14):'medium' ,(15,19): 'drastic',  (20,):'very_drastic' },
    'Stress': { (0,14):'Normal' , (15,18):'slight' , (19,25):'medium' ,(26,33): 'drastic',  (33,):'very_drastic' } 
    }