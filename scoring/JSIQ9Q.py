from Data import Data
import scoring.dictionary.JSIQ9Q as dictionary

class JSIQ9Q(Data):
    scores = {'raw' :  None }#

    def scoring_raw(self, score):
        section_1 = {
            "positive": {
                "total": 0,
                "average": 0
            },
            "negative": {
                "total": 0,
                "average": 0
            }
        }
        list = self.get_items_entirely()
        factorL = {
            "positive": 0,
            "negative": 0,
        }
        for i, key in enumerate(dictionary.section_1_items):
            answer = int(list[i].get('user_answered'))
            answer = answer if answer is not None else 0
            section_1[key] = answer
            subfactor = dictionary.section_1_factor[i + 1]
            factorL[subfactor] += 1
            section_1[subfactor]["total"] += answer
        section_1["positive"]["average"] = round(section_1["positive"]["total"] / (factorL["positive"]) , 1)
        section_1["negative"]["average"] = round(section_1["negative"]["total"] / (factorL["negative"]) , 1)
        score.set("section_1",section_1)

        section_2 = {"total": 0, "percentage": 0}
        counter = {"total":0}
        for factor in dictionary.section_2_factors:
            section_2[factor] = {"total": 0, "percentage": 0}
            counter[factor] = 0
        for i,item in enumerate(list[30:], start=1):
            answer = int(item.get('user_answered'))
            answer = answer if answer is not None else 1
            if i in dictionary.reverse_scoring_numbers:
                answer = answer
            else:
                answer = 6 - answer
            section_2["total"] += answer
            counter["total"] += 1
            for f in dictionary.factors[i]:
                section_2[f]["total"] += answer
                counter[f] += 1
        for factor in counter:
            if factor == "total":
                section_2["percentage"] = round((section_2["total"] / (counter[factor] * 5)) , 3)
                continue
            section_2[factor]["percentage"] = round((section_2[factor]["total"] / (counter[factor] * 5)) , 3)
            
        score.set("section_2",section_2)
        





