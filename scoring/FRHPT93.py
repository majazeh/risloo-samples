from Data import Data
import scoring.dictionary.FRHPT93 as dictionary

class FRHPT93(Data):
    scores = {'raw':None}
    def scoring_raw(self, score): 
        factors = {}
        for fi in dictionary.factor_list:
            factors[fi] = {
                'raw' : 0,
                'level': 'extremely_low'
            }
        identical = [0] * 6
        consecutive = [[None, None]]
        median = 0
        noneMedian = 0
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
            except:
                answer = None
            aIndex = answer - 1
            identical[aIndex] += 1
            ci = len(consecutive) - 1
            if(consecutive[ci][0] != aIndex):
                consecutive.append([aIndex, 0])
                ci += 1
            consecutive[ci][1] += 1
            index = i + 1
            if answer == 3 or answer == 4:
                median += 1
            if answer == 1 or answer == 6:
                noneMedian += 1
            s = (7 - answer) if index in dictionary.reverse_scoring_numbers else answer
            item_factors = dictionary.factors.get(index, ())
            for factor in item_factors:
                factors[factor]['raw'] += s
        
        for key in factors:
            factor = factors[key]
            level = self.getLevel(key, factor['raw'])
            factors[key]['level'] = level
            score.set('factors', factors)
        vi,vr = self.vrin()
        li,lr = self.lie_scale()
        di, dr = self.defensiveness_scale(factors)
        mi, mr = self.midpoint_responses(median, noneMedian)
        vdi, vdr = self.validity(identical, consecutive, median)
        indicators = {
            'validity': {
                'value': vdi,
                'level': vdr
            },
            'vrin' : {
                'value': vi,
                'level': vr
            },
            'lie_scale' : {
                'value': li,
                'level': lr
            },
            'defensiveness_scale' : {
                'value': di,
                'level': dr
            },
            'midpoint_responses' : {
                'value': mi,
                'level': mr
            },
        }
        score.set('indicators', indicators)
    def validity(self, identical, consecutive, median):
        identical = sorted(identical, reverse=True)
        firstIdentical = identical[0]
        consecutive.pop(0)
        consecutive = sorted([row[1] for row in consecutive], reverse=True)
        firstConsecutive = consecutive[0]
        if(firstIdentical >= 166):
            return [firstIdentical, 'exceeded identical responses threshold']
        elif (firstConsecutive >= 40):
            return [firstConsecutive, 'exceeded consecutive identical responses threshold']
        elif (median >= 31):
            return [median, 'exceeded median response threshold']
        return [0, None]

    def midpoint_responses(self, m, n):
        report = ''
        score = max(0, m - n)
        if score >= 45:
            report = 'extremely_high'
        elif score >= 35:
            report = 'very_high'
        elif score >= 30:
            report = 'high'
        elif score >= 20:
            report = 'average'
        elif score >= 16:
            report = 'low'
        elif score == 10:
            report = 'very_low'
        else:
            report = 'extremely_low'
        return [score, report]
    def defensiveness_scale(self, factors):
        score = 0
        report = ''
        for key in dictionary.defensiveness_scale:
            value = dictionary.defensiveness_scale[key]
            if value > 0 and factors[key]['raw'] >= value :
                score += 1
            elif value < 0 and factors[key]['raw'] <= value:
                score += 1
        if score >= 35:
            report = 'extremely_high'
        elif score >= 30:
            report = 'very_high'
        elif score >= 25:
            report = 'high'
        elif score >= 17:
            report = 'average'
        elif score >= 14:
            report = 'low'
        elif score == 10:
            report = 'very_low'
        else:
            report = 'extremely_low'
        return [score, report]
    def lie_scale(self):
        score = 0
        report = ''
        for v in dictionary.lie_scale:
            item = self.get_items_entirely()[v - 1]
            answer = int(item.get('user_answered'))
            score += answer
        if score >= 28:
            report = 'extremely_high'
        elif score >= 26:
            report = 'very_high'
        elif score >= 23:
            report = 'high'
        elif score >= 20:
            report = 'average'
        elif score >= 17:
            report = 'low'
        elif score == 12:
            report = 'very_low'
        else:
            report = 'extremely_low'
        return [score, report]
    def vrin(self):
        diffs = 0
        report = ''
        for v in dictionary.doubles:
            fi,si = v
            f = self.get_items_entirely()[fi -1]
            s = self.get_items_entirely()[si -1]
            fAnswer = int(f.get('user_answered'))
            sAnswer = int(s.get('user_answered'))
            diff = abs(fAnswer - sAnswer)
            diffs += diff
        if diffs >= 12:
            report = 'extremely_low'
        elif diffs >= 9:
            report = 'very_low'
        elif diffs >= 7:
            report = 'low'
        elif diffs >= 5:
            report = 'average'
        elif diffs >= 3:
            report = 'high'
        elif diffs == 2:
            report = 'very_high'
        else:
            report = 'extremely_high'
        return [diffs, report]
    
    def getLevel(self, key, raw):
        mean, sd = dictionary.norms[key]
        if raw >= round(mean + (sd * 2), 3):
            return 'extremely_high'
        elif raw >= round(mean + (sd * 1.5), 3):
            return 'very_high'
        elif raw >= round(mean + (sd * .75), 3):
            return 'high'
        elif raw > round(mean - (sd * .75), 3):
            return 'average'
        elif raw > round(mean - (sd * 1.5), 3):
            return 'low'
        elif raw > round(mean - (sd * 2), 3):
            return 'very_low'
        else:
            return 'extremely_low'

                