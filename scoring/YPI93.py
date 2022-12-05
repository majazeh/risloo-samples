from Data import Data
import scoring.dictionary.YPI93 as dictionary

class YPI93(Data):
    scores = {'raw':None}
 
    def scoring_raw(self, score): 
        iScore = {}
        raw={
                "father" : 0,
                "mother" : 0,
                "third" : 0,
            }
        all_items  = self.get_items_entirely()

        for i in dictionary.factors:
            iScore[i] = {
                "father" : 0,
                "mother" : 0,
                "third" : 0,
            }
        mod = ["father", "mother", "third"]
        for i in range(72):
            for j in range(3):
                index = (i * 3) + j
                item = all_items[index]
                answer = int(item.get('user_answered'))
                factor = dictionary.items[i+1]
                iScore[factor][mod[j]] += answer
                raw[mod[j]] += answer
        
        for i in dictionary.factors:
            score.set(i, iScore[i])
        score.set('raw', raw)
            
            