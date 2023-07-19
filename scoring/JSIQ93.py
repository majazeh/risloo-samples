from Data import Data
import scoring.dictionary.JSIQ93 as dictionary

class JSIQ93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        total = 0
        section_1 = {"total": 0}
        section_2 = {"total": 0}
        for key in dictionary.section_2_factors:
            section_2[key] = 0
        list = self.get_items_entirely()
        for i, key in enumerate(dictionary.section_1_items):
            answer = int(list[i].get('user_answered'))
            answer = answer if answer is not None else 0
            section_1["total"] += answer
            total += answer
            section_1[key] = answer
        
        for i,item in enumerate(list[30:], start=1):
            answer = int(item.get('user_answered'))
            answer = answer if answer is not None else 1
            total += answer
            section_2["total"] += answer
            for f in dictionary.factors[i]:
                section_2[f] += answer
            
        score.set("total",total)
        score.set("section_1",section_1)
        score.set("section_2",section_2)


        
     