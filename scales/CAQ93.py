from Data import Data
import scales.dictionary.CAQ93 as dictionary

class CAQ93(Data):
    scores = {'raw':None, 'norm' : None}
 
    def scoring_raw(self, score): 
        score.set(dictionary.factors_name,0)
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                answer = 2
                continue
            
            key = i + 1
            factor = dictionary.factors.get(key)
            weight = 2 if answer == factor[1] else (1 if answer == 2 else 0)
            if(weight != 0):
                score.increase('raw_' + factor[0], weight)
                score.increase('raw_result', weight)
                if(key <= 20):
                    score.increase('hidden_anxiety', weight)
                else:
                    score.increase('obvious_anxiety', weight)
    
    def scoring_norm(self, score): 
        gender = 'woman' if self.prerequisite('gender', 'user_answered') == 1 else 'man'
        result = score.get('raw_result')
        for key in dictionary.norm:
            if(result >= dictionary.norm[key][gender]):
                score.set('result', key)
                break
        level = 0
        result = score.get('result')
        if(result <= 3): level = 0
        elif(result <= 6): level = 1
        elif(result <= 7): level = 2
        else: level = 3
        score.set('anxiety_level', level)
        for factor in ['c', 'l', 'o', 'q3', 'q4']:
            score.set(factor, self.find_norm(score.get('raw_' + factor), factor))


    def find_norm(self, raw, factor):
        i = 0
        while i < len(dictionary.norms[factor]):
            if (dictionary.norms[factor][i] != None):
                if(raw >= dictionary.norms[factor][i]):
                    return 10 - i
            i += 1
            
            

                