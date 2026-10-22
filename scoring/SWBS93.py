from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SWBS93 as dictionary

# SWBS — مقیاس سلامت معنوی پولوتزین و الیسون: 20 گویه، گزینه‌های 1 تا 5 («کاملاً مخالفم» تا
# «کاملاً موافقم») با همان ارزش؛ گویه‌های معکوس (dictionary.reverse_scoring_numbers) 6 − پاسخ.
# فقط نمرهٔ کل: 20..100.
#
# نمرهٔ کل به‌صورت {raw, percent} زیر کلید total برمی‌گردد که ریسلو آن را به `total_raw` و
# `total_percent` تخت می‌کند. percent سهم نمره از بیشینه است (خام ÷ 100)، کسری 0..1 با سه رقم
# اعشار، نیمه رو به بالا، با تقسیم دقیق دهدهی — تصمیم پژوهشگر، 2026-10-21. هنجار نیست.
#
# گویهٔ بی‌پاسخ یا ناخوانا چیزی نمی‌افزاید و بیشینه را کم نمی‌کند. هیچ آلرتی ساخته نمی‌شود.

MAX = 100


class SWBS93(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i + 1 in dictionary.reverse_scoring_numbers:
                    answer = 6 - answer
                raw += answer
            except:
                pass
        score.set('total', {'raw': raw, 'percent': percent(raw, MAX)})


def percent(mark, top):
    """سهم نمره از بیشینه، سه رقم اعشار، نیمه رو به بالا."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
