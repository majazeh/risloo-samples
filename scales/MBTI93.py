from scales.MBTI9A import MBTI9A
import scales.dictionary.MBTI93 as dictionary

class MBTI93(MBTI9A):
    scores = {'raw' :  None, 'report' : None}
    def scoring_raw(self, score):
        score.set(dictionary.factors_name, 0)
        for i, item in self.items():
            answer = int(item.get('user_answered'))
            try:
                factor = dictionary.factors[answer][i + 1]
                score.increase(factor[0], factor[1]) if factor else None
            except:
                pass
