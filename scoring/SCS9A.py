from decimal import Decimal, ROUND_HALF_UP

from Data import Data

# SCS — مقیاس خودکنترلی تانجنی، فرم ۱۳ سوالی. 13 items, options 1..5, no factors; total 13..65.
# Option 1 is «همیشه در مورد من صدق می‌کند» and option 5 «به هیچ وجه …». Items 1, 6, 8, 11 are
# direct and scored 6 - option (5..1); items 2, 3, 4, 5, 7, 9, 10, 12, 13 are reversed and scored
# as the option number (1..5). A higher score means more self-control, as in the operational plan
# — researcher's decision, 2026-10-21; until then the direction was the other way round.
#
# The total is returned as {raw, percent} under the key `total`, which Risloo flattens to
# `total_raw` and `total_percent`. percent is the share of the fixed maximum (raw / 65),
# a fraction 0..1 kept to 3 decimals with halves rounded up, computed with Decimal —
# researcher's decision, 2026-10-19. It is not a norm.
#
# An unanswered or unreadable item adds nothing and does not shrink the maximum; an entirely
# unanswered sheet gets raw 0 and percent 0.0. No alert is produced.

DIRECT = (1, 6, 8, 11)
MAX = 65


class SCS9A(Data):
    scores = {'raw': None}

    def scoring_raw(self, score):
        raw = 0
        for i, item in self.items():
            try:
                answer = int(item.get('user_answered'))
                if i + 1 in DIRECT:
                    raw += 6 - answer
                else:
                    raw += answer
            except:
                pass
        score.set('total', {'raw': raw, 'percent': percent(raw, MAX)})


def percent(mark, top):
    """Share of the fixed maximum, 3 decimals, halves up."""
    return float((Decimal(mark) / Decimal(top)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP))
