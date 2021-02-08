from Data import Data
import scales.dictionary._16PF9A as dictionary

class _16PF9A(Data):
    scores = {'raw':None, 'norm': None}
 
    def scoring_raw(self, score): 
        score.set(dictionary.factors_name,0)
        score.set('status', 'valid')
        b_score = 0
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                answer = None

            if(i < 2 or i == 186):
                if(i == 186 and answer != 1):
                    score.set('status', 'invalid')
                continue
            key = i + 1
            detail = dictionary.factors.get(key)
            factor_title = detail[0].lower()
            if(factor_title == 'b'):
                if(answer == detail[1]):
                    score.increase('raw_' + factor_title)
                pass
            else:
                if(detail[1] == answer):
                    score.increase('raw_' + factor_title, 2)
                elif(answer == 2 or answer == None):
                    score.increase('raw_' + factor_title)
                    ++b_score

        if(b_score >= 53):
            score.set('status', 'invalid')
    
    def scoring_norm(self, score): 
        gender = self.prerequisite('gender', 'user_answered')
        norm = dictionary.norm.get('woman' if gender != '2' else 'men')
        for fi in dictionary.f:
            factor = fi.upper()
            selective_norm = norm.get(factor)
            for level in selective_norm:
                if(score.get('raw_' + fi) >= level):
                    score.set(fi, selective_norm.get(level))
                    break

                