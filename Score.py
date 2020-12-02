class Score:
    def __init__(self):
        self.__score = {}
        pass
    
    def increase(self, factor, weight = 1):
        if factor in self.__score:
            self.__score[factor] += weight
        else:
            self.__score [factor] = weight

    def set(self, key, value):
        if(isinstance(key, str)):
            self.__score[key] = value
        else:
            for k in key:
                self.__score[k] = value

    def get(self, key = None):
        if (key != None):
            if key in self.__score:
                result = self.__score[key]
            else:
                result = None
        else:
            result = self.__score
        return result

    def tree(self, tree = None):
        if(tree == None): return self
        if tree in self.__score: return self.__score[tree]
        self.__score[tree] = Score()
        return self.__score[tree]

    
    def toDict(self):
        result = {}
        for key in self.__score:
            if (isinstance(self.__score[key], Score)):
                result[key] = self.__score[key].toDict()
            else:
                result[key] =  self.__score[key]
        return result