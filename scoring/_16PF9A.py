from Data import Data
import scoring.dictionary._16PF9A as dictionary

class _16PF9A(Data):
    scores = {'raw':None, 'norm': None}
 
    def scoring_raw(self, score): 
        factors = {}
        for fi in dictionary.f:
            factors[fi] = {
                'raw' : 0,
                'value': 0
            }
        score.set('status', 'valid')
        score.set('b_count', 0)
        b_score = 0
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                answer = None

            if(i < 2 or i == 186):
                if(i == 186 and answer != 1):
                    score.set('status', 'invalid_final')
                continue
            key = i + 1
            detail = dictionary.factors.get(key)
            factor_title = detail[0].lower()
            if(factor_title == 'b'):
                if(answer == detail[1]):
                    factors[factor_title]['raw'] += 1
                pass
            else:
                if(detail[1] == answer):
                    factors[factor_title]['raw'] += 2
                elif(answer == 2 or answer == None):
                    factors[factor_title]['raw'] += 1
                    b_score += 1
        for fi in factors:
            score.set(fi, factors[fi])

        if(b_score >= 53):
            score.set('status', 'invalid_b' if score.get('status') == 'valid' else 'invalid_b_final')
        score.set('b_count', b_score)
    
    def scoring_norm(self, score):
        gender = int(self.prerequisite('gender', 'user_answered')) if self.prerequisite('gender', 'user_answered') != None else None
        if(gender == None or (gender != 1 and gender != 2)):
            raise ValueError("gender notfound")
        norm = dictionary.norm.get('woman' if gender == 1 else 'men')
        for fi in dictionary.f:
            itemObject = score.get(fi)
            factor = fi.upper()
            selective_norm = norm.get(factor)
            for level in selective_norm:
                if(itemObject['raw'] >= level):
                    itemObject['value'] = selective_norm.get(level)
                    print(fi, itemObject)
                    break

                