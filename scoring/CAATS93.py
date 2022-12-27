from Data import Data

from .MBTI9A import MBTI9A as MBTI
from .Raven93 import Raven93 as Raven
from .GMIT93 import GMIT93 as GMIT
from .RIASEC93 import RIASEC93 as RIASEC

class CAATS93(Data):
    scores = {'raw':None, 'mbti': 'mbti', 'raven': 'raven', 'gmit':'gmit', 'riasec':'riasec'}
 
    def __init__(self, data, type = 'raw'):
        super(CAATS93, self).__init__(  data, type )
        self.all_items  = self.get_items_entirely()

    def scoring_raw(self, score): 
        pass
    
    def scoring_mbti(self, score):
        virtual_items = {"items" : self.all_items[358:418]}
        mbti = MBTI(data = virtual_items  , type = 'object')
        
        mbti_scores = mbti.scoring().toDict()
        
        for key in mbti_scores.keys():
            score.set(key , mbti_scores[key])
    
    def scoring_raven(self, score):
        virtual_items = {"items" : self.all_items[418:478], "prerequisites": self.get_prerequisites_entirely()}
        raven = Raven(data = virtual_items  , type = 'object')
        
        raven_scores = raven.scoring().toDict()
        
        for key in raven_scores.keys():
            score.set(key , raven_scores[key])

    def scoring_gmit(self, score):
        virtual_items = {"items" : self.all_items[478:558]}
        gmit = GMIT(data = virtual_items  , type = 'object')
        
        gmit_scores = gmit.scoring().toDict()
        
        for key in gmit_scores.keys():
            score.set(key , gmit_scores[key])

    def scoring_riasec(self, score):
        virtual_items = {"items" : self.all_items[558:786]}
        riasec = RIASEC(data = virtual_items  , type = 'object')
        
        riasec_scores = riasec.scoring().toDict()
        
        for key in riasec_scores.keys():
            score.set(key , riasec_scores[key])


                