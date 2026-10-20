from decimal import Decimal, ROUND_HALF_UP

from Data import Data
import scoring.dictionary.SAM93 as dictionary


class SAM93(Data):
    scores = {"raw": None}

    # Total and four factors, each as {raw, percent}, which Risloo flattens to
    # `total_raw` / `total_percent` and `<factor>_raw` / `<factor>_percent`.
    # Option 1 (اصلا) scores 0 … option 5 (خیلی زیاد) scores 4; no reverse items.
    # `percent` is the share of the fixed maximum (raw / 76, 28, 16, 16, 16), a fraction
    # kept to 3 decimals with halves rounded up (researcher decision, 2026-10-19); not a norm.
    # The level and its stored band still come from the raw total, capped at 59.
    def scoring_raw(self, score):
        raws = {}
        for i, item in self.items():
            try:
                answer = int(item.get("user_answered"))
                factors = dictionary.factors[i + 1]

                raws[dictionary.total] = raws.get(dictionary.total, 0) + answer - 1
                for factor in factors:
                    raws[factor] = raws.get(factor, 0) + answer - 1

            except:
                pass

        for factor in dictionary.factors_names:
            raw = raws.get(factor)
            score.set(factor, {"raw": raw, "percent": percent(raw, dictionary.maxes[factor])})

        raw_score = raws.get(dictionary.total)
        interpretation = self.get_level_interpretation(
            raw_score if raw_score < 59 else 59
        )
        score.set("interpretation_level", interpretation[0])
        score.set("percentage_interpretation", interpretation[1])

    def get_level_interpretation(self, raw_score):
        intervals = list(dictionary.level_interpretation.keys())

        for interval in intervals:
            if interval[0] <= raw_score <= interval[1]:
                return dictionary.level_interpretation[interval]

        else:
            return None


def percent(raw, top):
    """Share of the maximum, 3 decimals, halves up; a score that was not produced has none."""
    if raw is None:
        return None
    return float((Decimal(raw) / Decimal(top)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))
