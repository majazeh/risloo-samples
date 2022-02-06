f1 = 'interaction'
f2 = 'structure'

factors_names = (f1,f2)
option_numbers = 5

interpretation_conditions = [
    { "interaction_range" : (6,18), "structure_range" : (6,18), "result": 'aimless/undirected'},
    { "interaction_range" : (6,18), "structure_range" : (19,30), "result": 'inconsistent'},
    
    { "interaction_range" : (19,30), "structure_range" : (6,18), "result": 'messy/chaos'},
    { "interaction_range" : (19,30), "structure_range" : (19,30), "result": 'worthy'},
]

        
        




