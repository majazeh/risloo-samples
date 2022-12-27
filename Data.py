from loader import loader
from Score import Score
from Interpret import Interpret

class Data(object):
    scores = {'raw' : None}
    def __init__(self, data, type = 'raw'):
        self.__data = loader(data, type).load()
        self.score = Score()
        self.interpret = Interpret()

        if 'prerequisites' in self.__data:
            prerequisites = self.__data['prerequisites']
            self.__prerequisites = {}
            for prerequisite in prerequisites:
                self.__prerequisites[prerequisite.get('label')] = prerequisite

    
    def scoring(self):
        for method in self.scores:
            getattr(self, 'scoring_' + method)(self.score.tree(self.scores[method]))
        return self.score


    def interpreting(self):
        for method in self.interprets:
            getattr(self, 'interpreting_' + method)(self.interpret)
    
        return self.interpret


    def items(self):
        return enumerate(self.__data['items'])
    
    def get_items_entirely(self):
        return self.__data['items']
    
    def get_prerequisites_entirely(self):
        return self.__data['prerequisites']


    def prerequisites(self):
        return self.__prerequisites

    
    def prerequisite(self, label, key = None):
        result = self.__prerequisites.get(label)
        return result.get(key) if key != None else result
