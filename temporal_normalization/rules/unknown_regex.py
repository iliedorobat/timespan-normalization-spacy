from temporal_normalization.rules.timespan_regex import (
    REGEX_OR,
    CASE_INSENSITIVE,
)

# -------------------------
# UNKNOWN REGEX
# -------------------------

"""
Regular expressions for those time intervals that are stored
as an unknown time period
"""
UNKNOWN = (
        CASE_INSENSITIVE
        + "^("
        + "-"
        + REGEX_OR + r"4/4 sec\."
        + REGEX_OR + r"17 nov\. 375\-9 aug\. 378 a\.chr\."
        + REGEX_OR + r"1884 martie 28/aprilie 09"
        + REGEX_OR + r"189-45"
        + REGEX_OR + r"al doile afert al s1900"
        + REGEX_OR + r"an[ ]?\d{1,2}[\?]?"
        + REGEX_OR + r"cultura inca sau chachapoya\?"
        + REGEX_OR + r"datat"
        + REGEX_OR + r"dinastia xxv"
        + REGEX_OR + r"dinastia xxvi \(dinastia saita\)"
        + REGEX_OR + r"dinastia xxvi \(perioada saita\)"
        + REGEX_OR + r"dinastia xxvii \(prima stapanire persana\)"
        + REGEX_OR + r"nesemnat"
        + REGEX_OR + r"disparuta din uz si din zona; existenta in muzee"
        + REGEX_OR + r"epoca severica tarzie"
        + REGEX_OR + r"grupa a iv-a"
        + REGEX_OR + r"grupa a v-a"
        + REGEX_OR + r"grupa iii"
        + REGEX_OR + r"grupa iv"
        + REGEX_OR + r"grupa v"
        + REGEX_OR + r"la tene"
        + REGEX_OR + r"lama de secol xvi/xvii, garda si manerul ulterioare"
        + REGEX_OR + r"leat 7208 \(1699-1700\)"
        + REGEX_OR + r"mai, dni 15, leat 7232"
        + REGEX_OR + r"mesiata.*"
        + REGEX_OR + r"fev\. dni 2 leat 7157"
        + REGEX_OR + r"iulie 28"
        + REGEX_OR + r"iunie 01"
        + REGEX_OR + r"iunie 20, leat 7173 \(1665\)"
        + REGEX_OR + r"iunie, dni 2, leat 7235"
        + REGEX_OR + r"august 04"
        + REGEX_OR + r"oct\. 10 dni, leat 1730"
        + REGEX_OR + r"octombrie 23, 1777"
        + REGEX_OR + r"noiembrie 22"
        + REGEX_OR + r"noiembrie 24"
        + REGEX_OR + r"perioada lui carol x al frantei"
        + REGEX_OR + r"perioada domniei regelui carol al ii-lea"
        + REGEX_OR + r"perioada regelui carol al ii-lea"
        + REGEX_OR + r"regatul nou\?"
        + REGEX_OR + r"21/2, sc\.i, a\.c\."
        + REGEX_OR + r"21/2; sc i a\.c\."
        + REGEX_OR + r"286/5-282/1"
        + REGEX_OR + r"286/5-282/1 a\. chr"
        + REGEX_OR + r"15\(\…\)4"
        + REGEX_OR + r"154\(\…\)"
        + REGEX_OR + r"158\(\…\)"
        + REGEX_OR + r"162\(\?\)"
        + REGEX_OR + r"16\[\ ]"
        + ")$"
)
