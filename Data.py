from loader import loader
from Score import Score
class Data:
    scores = {'raw' : None}
    def __init__(self, data, type = 'raw'):
        self.__data = loader(data, type).load()
        self.score = Score()
    
    def scoring(self):
        for method in self.scores:
            getattr(self, 'scoring_' + method)(self.score.tree(self.scores[method]))
        return self.score
    
    def items(self):
        return enumerate(self.__data['items'])
