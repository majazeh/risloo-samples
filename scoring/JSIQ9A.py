from Data import Data
import scoring.dictionary.JSIQ9A as dictionary

class JSIQ9A(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        total = 0
        section_1 = {"total": 0}
        section_2 = {"total": 0}
        section_3 = {}
        for key in dictionary.section_2_factors:
            section_2[key] = 0
        list = self.get_items_entirely()
        for i, key in enumerate(dictionary.section_1_items):
            answer = int(list[i].get('user_answered'))
            answer = answer if answer is not None else 0
            section_1["total"] += answer
            total += answer
            section_1[key] = answer
        
        for i,item in enumerate(list[20:100], start=1):
            answer = int(item.get('user_answered'))
            answer = answer if answer is not None else 1
            total += answer
            section_2["total"] += answer
            for f in dictionary.factors[i]:
                section_2[f] += answer
        for i,item in enumerate(list[100:], start=1):
            answer = int(item.get('user_answered'))
            section_3["q_" + str(i)] = "agreement" if answer == 1 else "disagreement"
        score.set("total",total)
        score.set("section_1",section_1)
        score.set("section_2",section_2)
        score.set("section_3",section_3)


        
     