from decimal import Decimal, ROUND_HALF_UP

from Data import Data

# FMPQ — پرسشنامه خودکارآمدی اخلاقی: 13 گویه، گزینه‌های 1 تا 4، بدون مولفه و بدون معکوس؛ نمرهٔ کل 13..52.
#
# نمرهٔ کل به‌صورت {raw, percent} زیر کلید total برمی‌گردد که ریسلو آن را به `total_raw` و
# `total_percent` تخت می‌کند. percent سهم نمره از بیشینه است (خام ÷ 52)، کسری 0..1 با سه رقم
# اعشار، نیمه رو به بالا، با تقسیم دقیق دهدهی — تصمیم پژوهشگر، 2026-10-19. هنجار نیست.
# percentage چهاررقمی که پیش‌تر برمی‌گشت، دیگر برگردانده نمی‌شود.
#
# سؤال بی‌پاسخ یا ناخوانا چیزی اضافه نمی‌کند و بیشینه را کم نمی‌کند؛ پاسخ‌نامهٔ تمام‌بی‌پاسخ
# خام 0 و درصد 0.0 می‌گیرد. آلرتی ساخته نمی‌شود.

MAX = 52


class FMPQ93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():
            try:
                raw += int(item.get('user_answered'))
            except:
                pass
        score.set('total', {'raw': raw, 'percent': percent(raw, MAX)})


def percent(mark, top):
    """سهم نمره از بیشینه، سه رقم اعشار، نیمه رو به بالا."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
