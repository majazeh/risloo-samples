from Data import Data
import scoring.dictionary.YPI93 as dictionary

class YPI93(Data):
    scores = {'raw':None}
 
    def scoring_raw(self, score): 
        iScore = {}

        all_items  = self.get_items_entirely()
        fP = {}
        for i in range(72):
            factor = dictionary.items[i+1]
            if factor in fP:
                fP[factor] += 6
            else: 
                fP[factor] = 6
        for i in dictionary.factors:
            iScore[i] = {
                "father" : {
                    "score": 0,
                    "percentage": 0,
                },
                "mother" : {
                    "score": 0,
                    "percentage": 0,
                },
            }
        mod = ["father", "mother"]
        for i in range(72):
            for j in range(2):
                index = (i * 2) + j
                item = all_items[index]
                answer = int(item.get('user_answered'))
                factor = dictionary.items[i+1]
                if factor == dictionary.f1:
                    answer = 7 - answer
                iScore[factor][mod[j]]["score"] += answer
        
        for i in dictionary.factors:
            iScore[i]['father']["percentage"] = round(iScore[i]['father']["score"] / fP[i], 4)
            iScore[i]['mother']["percentage"] = round(iScore[i]['mother']["score"] / fP[i], 4)
            score.set(i, iScore[i])
            
            