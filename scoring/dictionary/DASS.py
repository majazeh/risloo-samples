factors_names = ('stress' ,'anxiety' , 'depression')


factors_interval = { 
    'depression': { (0,9):0 , (10,13):1 , (14,20):2 ,(21,27): 3,  (28,):4 },
    'anxiety': { (0,7):0 , (8,9):1 , (10,14):2 ,(15,19): 3,  (20,):4 },
    'stress': { (0,14):0 , (15,18):1 , (19,25):2 ,(26,33): 3,  (33,):4 } 
    }