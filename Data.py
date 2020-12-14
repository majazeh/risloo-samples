from loader import loader
from Score import Score
class Data:
    scores = {'raw' : None}
    def __init__(self, data, type = 'raw'):
        self.__data = loader(data, type).load()
        self.score = Score()
        prerequisites = self.__data['prerequisites']
        self.__prerequisites = {}
        for prerequisite in prerequisites:
            self.__prerequisites[prerequisite.get('label')] = prerequisite

    
    def scoring(self):
        for method in self.scores:
            getattr(self, 'scoring_' + method)(self.score.tree(self.scores[method]))
        return self.score
    
    def items(self):
        return enumerate(self.__data['items'])
    
    def prerequisites(self):
        return self.__prerequisites
    
    def prerequisite(self, label, key = None):
        result = self.__prerequisites.get(label)
        return result.get(key) if key != None else result