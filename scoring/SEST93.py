from decimal import Decimal, ROUND_HALF_UP

from Data import Data

# SEST — مقیاس تفکر وجودی شرر: 11 گویه، شش گزینه با ارزش «نمی‌دانم» 0، «هرگز یا به ندرت» 1،
# «گاهی» 2، «اغلب» 3، «تقریبا همیشه» 4 و «همیشه» 5 (شمارهٔ گزینه − 1). فقط نمرهٔ کل: 0..55.
# صفر بودن «نمی‌دانم» قاعدهٔ فعلی است و دست نخورده است.
#
# نمرهٔ کل به‌صورت {raw, percent} زیر کلید total برمی‌گردد که ریسلو آن را به `total_raw` و
# `total_percent` تخت می‌کند. percent سهم نمره از بیشینه است (خام ÷ 55)، کسری 0..1 با سه رقم
# اعشار، نیمه رو به بالا، با تقسیم دقیق دهدهی — تصمیم پژوهشگر، 2026-10-22. هنجار نیست.
#
# گویهٔ بی‌پاسخ یا ناخوانا چیزی نمی‌افزاید و بیشینه را کم نمی‌کند. هیچ آلرتی ساخته نمی‌شود.

MAX = 55


class SEST93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                raw += answer - 1
            except:
                pass
        score.set('total', {'raw': raw, 'percent': percent(raw, MAX)})


def percent(mark, top):
    """سهم نمره از بیشینه، سه رقم اعشار، نیمه رو به بالا."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
