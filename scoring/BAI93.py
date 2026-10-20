from decimal import Decimal, ROUND_HALF_UP

from Data import Data

# BAI — آزمون اضطراب بک: 21 گویه، گزینه‌های 1 تا 4 با ارزش 0 تا 3 (پاسخ − 1)، بدون معکوس؛ نمرهٔ کل 0..63.
#
# نمرهٔ کل به‌صورت {raw, percent} زیر کلید total برمی‌گردد که ریسلو آن را به `total_raw` و
# `total_percent` تخت می‌کند. percent سهم نمره از بیشینه است (خام ÷ 63)، کسری 0..1 با سه رقم
# اعشار، نیمه رو به بالا، با تقسیم دقیق دهدهی — تصمیم پژوهشگر، 2026-10-20. هنجار نیست.
#
# range درجهٔ اضطراب است، همان مرزهای نمره‌گذاری پیشین در مدل ریسلو: 0 تا 7 → 0، 8 تا 15 → 1،
# 16 تا 25 → 2، 26 به بالا → 3.
#
# گویهٔ بی‌پاسخ یا ناخوانا چیزی نمی‌افزاید و بیشینه را کم نمی‌کند. هیچ آلرتی ساخته نمی‌شود.

MAX = 63
RANGES = ((7, 0), (15, 1), (25, 2))


class BAI93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():
            try:
                raw += int(item.get('user_answered')) - 1
            except:
                pass
        score.set('total', {'raw': raw, 'percent': percent(raw, MAX)})
        score.set('range', band(raw))


def band(raw):
    for top, level in RANGES:
        if raw <= top:
            return level
    return 3


def percent(mark, top):
    """سهم نمره از بیشینه، سه رقم اعشار، نیمه رو به بالا."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
