f1 = 'nutrition'
f2 = 'sleep'
f3 = 'sport'
f4 = 'awareness'
f5 = 'conflict_stress'
f6 = 'affection_management'
f7 = 'security'
f8 = 'disease_prevention'
f9 = 'god_relation'

factorList = [f1,f2,f3,f4,f5,f6,f7,f8,f9]
indicator = {
    f1: 35,
    f2: 66,
    f3: 74,
    f4: 85,
    f5: 93,
    f6: 101,
    f7: 108,
    f8: 113,
    f9: 120,
}

factors = {
}
currentFactorIndex = 0
currentFactor = factorList[currentFactorIndex]
currentIndex = indicator.get(currentFactor)
for i in range(120):
    if(i+1 > currentIndex):
        currentFactorIndex += 1
        currentFactor = factorList[currentFactorIndex]
        currentIndex = indicator.get(currentFactor)
    factors[i+1] = currentFactor

reverse = [
    3,8,9,
    10,12,13,14,19,
    20,24,25,26,
    36,38,
    40,41,44,45,47,48,49,
    50,51,52,53,54,55,56,57,58,59,
    62,63,75,76,77,79,
    80,81,82,83,86,87,88,89,
    90,91,92,93,
    108,111
]