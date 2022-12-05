from Data import Data
import scoring.dictionary.RIASEC93 as dictionary

class RIASEC93(Data):
    scores = {'raw' :  None }# 
        
    def scoring_raw(self, score):
        all_items  = self.get_items_entirely()
        factors = [[dictionary.r, all_items[0:11] + all_items[66:77] + all_items[132:146] + all_items[216:217] + all_items[222:223]],
        [dictionary.i, all_items[11:22] + all_items[77:88] + all_items[146:160] + all_items[217:218] + all_items[223:224]],
        [dictionary.a, all_items[22:33] + all_items[88:99] + all_items[160:174] + all_items[218:219] + all_items[224:225]],
        [dictionary.s, all_items[33:44] + all_items[99:110] + all_items[174:188] + all_items[219:220] + all_items[225:226]],
        [dictionary.e, all_items[44:55] + all_items[110:121] + all_items[188:202] + all_items[220:221] + all_items[226:227]],
        [dictionary.c, all_items[55:66] + all_items[121:132] + all_items[202:216] + all_items[221:222] + all_items[227:228]]]
        for i, factor in enumerate(factors):
            score.set(factor[0], 0)
            for j, item in enumerate(factor[1]):
                answer = int(item.get('user_answered'))
                if(j < 36 and answer == 1):
                    score.increase(factor[0])
                elif(j >= 36):
                    score.increase(factor[0], answer)

            
        
            