factors_name = ('Stress' ,'Anxiety' , 'Depression')
factors_intensity = ('Stress_instensity' ,'Anxiety_instensity' , 'Depression_instensity')


factors_interval = { 
    'Depression': { (0,9):'Normal' , (10,13):'slight' , (14,20):'medium' ,(21,27): 'drastic',  (28,):'very_drastic' },
    'Anxiety': { (0,7):'Normal' , (8,9):'slight' , (10,14):'medium' ,(15,19): 'drastic',  (20,):'very_drastic' },
    'Stress': { (0,14):'Normal' , (15,18):'slight' , (19,25):'medium' ,(26,33): 'drastic',  (33,):'very_drastic' } 
    }