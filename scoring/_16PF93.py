from Data import Data
import scoring.dictionary._16PF9A as dictionary

class _16PF93(Data):
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

        if(b_score >= 59):
            score.set('status', 'invalid_b' if score.get('status') == 'valid' else 'invalid_b_final')
        score.set('b_count', b_score)
    
    def scoring_norm(self, score):
        gender = int(self.prerequisite('gender', 'user_answered')) if self.prerequisite('gender', 'user_answered') != None else None
        if(gender == None or (gender != 1 and gender != 2)):
            raise ValueError("gender notfound")
        for factor in dictionary.vx:
            raw = score.get(factor).get('raw')
            norm = 0
            for level, value in enumerate(dictionary.vx[factor]):
                if value == None: continue
                if(raw <= value): 
                    norm = level + 1
                    break
            score.set(factor, {'raw': raw, 'value': norm})
        score.set('extraversion', (3 * score.get('a').get('value') + 4 * score.get('f').get('value') + 4 * score.get('h').get('value') - 4 * score.get('q2').get('value') + 17) / 10)
        
        score.set('anxiety', (-3 * score.get('c').get('value') - score.get('h').get('value') + score.get('l').get('value') + 3 * score.get('o').get('value') - score.get('q3').get('value') + 3 * score.get('q4').get('value') + 44) / 10)
        
        if gender == 2:
            score.set('inflexibility', (-2 * score.get('a').get('value') + 2 * score.get('f').get('value') - 6 * score.get('i').get('value') - 4 * score.get('m').get('value') - 2 * score.get('q1').get('value') + 121) / 10)
        else:
            score.set('inflexibility', (-score.get('a').get('value') + 4 * score.get('e').get('value') + 2 * score.get('f').get('value') - 6 * score.get('i').get('value') + 2 * score.get('l').get('value') - 4 * score.get('m').get('value') + 72) / 10)
        
        if gender == 2:
            score.set('independence', (5 * score.get('e').get('value') - score.get('g').get('value') + 3 * score.get('h').get('value') + 2 * score.get('l').get('value') - score.get('n').get('value') - 2 * score.get('o').get('value') + 2 * score.get('q1').get('value') + score.get('q2').get('value') + 6) / 10)
        else:
            score.set('independence', (5 * score.get('e').get('value') - score.get('g').get('value') + 3 * score.get('h').get('value') + 2 * score.get('m').get('value') + 4 * score.get('q1').get('value') + score.get('q2').get('value') - 22) / 10)
            
        score.set('selfcontrol', (7 * score.get('g').get('value') + 5 * score.get('q3').get('value') - 11) / 10)

        score.set('adjustment', (score.get('b').get('value') + 3 * score.get('c').get('value') + 2 * score.get('e').get('value') + 4 * score.get('f').get('value') + score.get('g').get('value') - score.get('h').get('value') - 2 * score.get('i').get('value') - 3 * score.get('o').get('value') - score.get('q1').get('value') - 4 * score.get('q4').get('value') + 44) / 10)        

        score.set('leadership', (score.get('b').get('value') + score.get('c').get('value') + score.get('e').get('value') + 2 * score.get('f').get('value') + 2 * score.get('g').get('value') + 2 * score.get('h').get('value') - score.get('i').get('value') - score.get('m').get('value') + score.get('n').get('value') - 2 * score.get('o').get('value') + 2 * score.get('q3').get('value') - score.get('q4').get('value') + 17) / 10)
        
        score.set('creativity', (-3 * score.get('a').get('value') + 3 * score.get('b').get('value') + 2 * score.get('e').get('value') - 3 * score.get('f').get('value') + 2 * score.get('h').get('value') + 3 * score.get('i').get('value') + 2 * score.get('m').get('value') - 2 * score.get('n').get('value') + 2 * score.get('q1').get('value') + 3 * score.get('q2').get('value') + 6) / 10)
            

                