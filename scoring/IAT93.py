from decimal import Decimal, ROUND_HALF_UP

from Data import Data

# IAT — پرسشنامه اعتیاد به اینترنت کیمبرلی یانگ: 20 گویه، گزینه‌های 1 تا 5، بدون معکوس؛ نمرهٔ کل 20..100.
#
# نمرهٔ کل به‌صورت {raw, percent} زیر کلید total برمی‌گردد که ریسلو آن را به `total_raw` و
# `total_percent` تخت می‌کند. percent سهم نمره از بیشینه است (خام ÷ 100)، کسری 0..1 با سه رقم
# اعشار، نیمه رو به بالا، با تقسیم دقیق دهدهی — تصمیم پژوهشگر، 2026-10-19. هنجار نیست.
# میانگین پاسخ‌ها (خام ÷ 20) که پیش‌تر با نام percentage برمی‌گشت، دیگر برگردانده نمی‌شود.
#
# report سطح نمرهٔ خام است و تغییری نکرده: کمتر از 50 average_user، 50 تا 79 moderate_addiction،
# 80 به بالا severe_addiction.

MAX = 100

class IAT93(Data):
    scores = {'raw' :  None }# 
    
    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():   
            answer = int(item.get('user_answered')) 
            raw += answer
        score.set('total', {'raw': raw, 'percent': percent(raw, MAX)})
        score.set('report', 'severe_addiction')
        if(raw < 50):
            score.set('report', 'average_user')
        elif(raw < 80):
            score.set('report', 'moderate_addiction')


def percent(mark, top):
    """سهم نمره از بیشینه، سه رقم اعشار، نیمه رو به بالا."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
