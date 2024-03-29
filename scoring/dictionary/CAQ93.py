factors_names = (
    'c', 'l', 'o', 'q3', 'q4',
    'raw_c', 'raw_l', 'raw_o', 'raw_q3', 'raw_q4',
    'result', 'raw_result',
    'anxiety_level', 'hidden_anxiety', 'obvious_anxiety'
    )

factors = {
    1 : ['q3', 1],
    2 : ['q3', 3],
    3 : ['q3', 3],
    4 : ['q3', 1],
    5 : ['c', 1],
    6 : ['c', 3],
    7 : ['c', 1],
    8 : ['l', 1],
    9 : ['l', 3],
    10 : ['o', 3],
    11 : ['o', 3],
    12 : ['o', 1],
    13 : ['o', 1],
    14 : ['o', 3],
    15 : ['o', 1],
    16 : ['q4', 1],
    17 : ['q4', 3],
    18 : ['q4', 1],
    19 : ['q4', 3],
    20 : ['q4', 1],
    21 : ['q3', 1],
    22 : ['q3', 3],
    23 : ['q3', 3],
    24 : ['q3', 1],
    25 : ['c', 1],
    26 : ['c', 3],
    27 : ['c', 1],
    28 : ['l', 1],
    29 : ['l', 3],
    30 : ['o', 1],
    31 : ['o', 3],
    32 : ['o', 1],
    33 : ['o', 1],
    34 : ['o', 3],
    35 : ['o', 1],
    36 : ['q4', 1],
    37 : ['q4', 3],
    38 : ['q4', 1],
    39 : ['q4', 3],
    40 : ['q4', 1],
}

norm = {
    10 : {
    "women": 54,
    "man": 50
  },
  9 : {
    "women": 50,
    "man": 46
  },
  8 : {
    "women": 45,
    "man": 41
  },
  7 : {
    "women": 41,
    "man": 37
  },
  6 : {
    "women": 37,
    "man": 33
  },
  
  5 : {
    "women": 32,
    "man": 28
  },
  4 : {
    "women": 28,
    "man": 24
  },
  3 : {
    "women": 24,
    "man": 20
  },
  2 : {
    "women": 19,
    "man": 15
  },
 1 : {
    "women": 15,
    "man": 14
  }, 
  0 : {
    "women": 0,
    "man": 0
  }
}

norms = {
    'c' : [9, 8, 7, 6, 5, 4, 3, 2, 1,0],
    'l' : [7, None, 6, 5, 4, None, 3, 2, 1, 0],
    'o' : [18, 15, 14, 12, 10, 9, 7, 6, 4, 3, 2],
    'q3': [12, 11, 9, 7, 6, 5, 4, 3, 2, 1, 0],
    'q4' : [18, 16, 14, 13, 11, 9, 8, 6, 4, 3, 2]
}