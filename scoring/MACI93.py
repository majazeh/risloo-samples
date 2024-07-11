from Data import Data
import scoring.dictionary.MACI93 as dictionary

class MACI93(Data):
    scores = {'raw' :  'raw', "v": None , 'x' : 'raw', 'br': 'br', 'correction_x': None, 'correction_ad': None, 'correction_dd': None, 'correction_dc': None, 'status': None}# 
    
    def scoring_raw(self, score):
        gender = self.prerequisite('gender', 'user_answered')
        if(gender == None):
            raise ValueError("gender notfound")
        age = self.prerequisite('age', 'user_answered')
        if(age == None):
            raise ValueError("age notfound")
        age = int(age)
        if(age < 13 or age > 19):
            raise ValueError("age invalid")
        self.all_items  = self.get_items_entirely()
        self.scoringStatus = 0
        for i in dictionary.factors:
            score.set(i, 0)
        for i, item in self.items():   
            answer = int(item.get('user_answered'))
            try:
                factors = dictionary.raw_factor[i+1]
                lists = factors[answer - 1]
                for list in lists:
                    score.increase(list.get('factor'), list.get('weight'))
            except:
                pass

    def scoring_v(self, score):
        score.set('v', 0)
        if(int(self.all_items[113].get('user_answered')) == 1):
            score.increase('v')
        
        if(int(self.all_items[125].get('user_answered')) == 1):
            score.increase('v')
    def scoring_x(self, score):
        raw_x = (score.get('1') + score.get('2a')) * 1.5
        raw_x += (score.get('3') + score.get('4')+ score.get('7')) * 0.7
        raw_x += score.get('2b') * 2
        raw_x += score.get('6b') * 3
        raw_x += score.get('5') + score.get('6a')+ score.get('8a')+ score.get('8b')
        score.set('x', round(raw_x))
        
    def scoring_br(self, score):
        gender = 'male' if self.prerequisite('gender', 'user_answered') == 'male' else 'female'
        ageGroup = '13-15' if int(self.prerequisite('age', 'user_answered')) <= 15 else '16-19'
        
        brGroup = dictionary.br.get(gender).get(ageGroup)
        raw = self.score.get('raw')
        for i in dictionary.factors:
            rawScore = raw.get(i)
            score.set(i, 0)
            if(i == 'x'):
                list = dictionary.br.get('x')
            else:
                list = brGroup.get(i)
            for j in list:
                if(j.get('min') > rawScore):
                    break
                score.set(i, j.get('br'))
    def scoring_correction_x(self, score):
        listc = ['1','2a','2b','3','4','5','6a','6b','7','8a','8b','9']
        weight = 0
        for i in dictionary.correction_x:
            if(i.get('min') >= score.get('raw').get('x')):
                break
            weight = i.get('weight')
        for i in listc:
            sc = score.get('br').get(i)
            update = sc + weight
            if (update < 1):
                update = 1
            elif (update > 115):
                update = 115
            score.get('br').set(i, update)
            
    def scoring_correction_ad(self, score):
        listc = ['2a','2b','8b','9']
        ad = None
        ee = score.get('br').get('ee')
        ff = score.get('br').get('ff')
        if(ee >= 85 and ff < 85):
            ad = ff - 84
        elif (ff >= 85 and ee < 85):
            ad = ff - 84
        elif (ff >= 85 and ee >= 85):
            ad = (ee - 84) + (ff - 84)
        weight = 0
        for i in dictionary.correction_ad:
            if(i.get('min') > ad):
                break
            weight = i.get('weight')
        if(ad != None):
            for i in listc:
                sc = score.get('br').get(i)
                update = sc - weight
                if (update < 1):
                    update = 1
                elif (update > 115):
                    update = 115
                score.get('br').set(i, update)
    def scoring_correction_dd(self, score):
        listc = ['a','b','c','d','e','f','g','h','aa','ee','ff','gg']
        br = score.get('br')
        dd = br.get('y') - br.get('z')
        absdd = abs(dd)
        if(absdd > 4):
            weight = 0
            for i in dictionary.correction_dd:
                if(i.get('min') >= dd):
                    break
                weight = i.get('weight')
            for i in listc:
                sc = score.get('br').get(i)
                update = sc + weight
                if (update < 1):
                    update = 1
                elif (update > 115):
                    update = 115
                score.get('br').set(i, update)
                
    def scoring_correction_dc(self, score):
        maxdc = -100000
        maxfc = None
        dc = None
        finder = ['1','3','5','4','7','8a','2a','6b','8b','6a','2b']
        for i in finder:
            if(score.get('br').get(i) > maxdc):
                maxdc = score.get('br').get(i)
                maxfc = i
        if(maxfc == '4' or maxfc == '5' or maxfc == '7'):
            dc = 4
        elif (maxfc == '2b' or maxfc == '2a' or maxfc == '8b'):
            dc = -4
            
        if(dc != None):
            listc = ['a','b','g','ee','ff','gg']
            for i in listc:
                sc = score.get('br').get(i)
                update = sc + dc
                if (update < 1):
                    update = 1
                elif (update > 115):
                    update = 115
                score.get('br').set(i, update)
        
    def scoring_status(self, score):
        status = score.get('v')
        score.set('xstatus', 0)
        if(score.get('raw').get('x') > 589 or score.get('raw').get('x') < 201):
            score.set('xstatus', 2)
            status = 2
        up = False
        listc = ['1','2a','2b','3','4','5','6a','6b','7','8a','8b']
        for i in listc:
            if(score.get('br').get(i) >= 60):
                up = True
        score.set('brstatus', 0)
        if(up == False):
            score.set('brstatus', 2)
            status = 2
        score.set('status', status)
        