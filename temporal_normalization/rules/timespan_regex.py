# By using the <b>[?<=sentence]</b> construction, it will be matched
# any text after "sentence" ("sentence" is a word as example).

# -------------------------
# BASIC CONSTANTS
# -------------------------

ANY_WORDS = r"[\wăâîşșţțĂÂÎŞȘŢȚ]*"
REGEX_OR = "|"
# FIXME: Java value = "(?iu)"
CASE_INSENSITIVE = ""
REGEX_PUNCTUATION = r"[\.,;\?!\-\s]"
REGEX_PUNCTUATION_UNLIMITED = REGEX_PUNCTUATION + "*"

# The separator must always be of the shape "(\s+-\s+)"
REGEX_INTERVAL_DELIMITER = r"\s*(?:-|–|—)\s*"
# TODO: check the if changing the old expression introduces bugs
#  REGEX_INTERVAL_CONJUNCTION = r"\s*(?:-|–|—|([sşș]i))\s*"
REGEX_INTERVAL_CONJUNCTION = r"\s*(?:-|–|—|\b[sşș]i\b)\s*"
REGEX_INTERVAL_PREFIX = rf"(?:[iî]ntre|[iî]n\s*interval(?:ul|u)?)\s*"
REGEX_DATE_SEPARATOR = r"[\./\-\s]+"

# Regex for marking the start of the text
TEXT_START = (
        "("
        # + "?<=" + "("
        + "^" + REGEX_OR + r"\A" + REGEX_OR + r"[\.,;\?!\-(\[= ]+"
        # + ")"
        + ")"
)
# TEXT_START = r"(?:^|[\.,;?!\-\(\[= ]+)"

# Regex for marking the end of the text
TEXT_END = (
        "("
        # + "?=" + "("
        + "$" + REGEX_OR + r"\Z" + REGEX_OR + r"[\.,;\?!\-\)\] ]+"
        # + ")"
        + ")"
)

# # FIXME: ???
# TEXT_START = r"(?:(?<=^)|(?<=\A)|(?<=[\.,;\?!\-(\[= ]))"
# TEXT_END   = r"(?:(?=$)|(?=\Z)|(?=[\.,;\?!\-\)\] ]))"

# Regex for all possible values for Christum notation
# E.g.: "ch"; "ch."; "chr"; "chr."; "hr"; "hr."
REGEX_CHRISTUM = r"(ch[r]?|hr|c)[\. ]*"

# -------------------------
# AGE NOTATIONS
# -------------------------

# Anno Domini (After Christ)
# TODO: remove
# AGE_AD = (
#         TEXT_START
#         + CASE_INSENSITIVE
#         + "("
#         + "(" + r"e[\.]?n[\.]?" + ")" + REGEX_OR
#         + "(" + r"[dp][\. ]*" + REGEX_CHRISTUM + ")"
#         + ")"
#         + TEXT_END
# )
AGE_AD = r"(?<!\w)((?:e\.?n\.?)|(?:[dp][\. ]*(?:ch[r]?|hr|c)[\. ]*))(?!\w)"

# Before Christ
# TODO: remove
# AGE_BC = (
#         TEXT_START
#         + CASE_INSENSITIVE
#         + "("
#         + "(" + r"[iî][\.]?e[\.]?n[\.]?" + ")" + REGEX_OR
#         + "(" + r"[abiî][\. ]*" + REGEX_CHRISTUM + ")"
#         + ")"
#         + TEXT_END
# )
AGE_BC = r"(?<!\w)([abiî][\. ]*(?:ch[r]?|hr|c)[\. ]*)(?!\w)"

# Anno Domini / Before Christ notation wrapper

CHRISTUM_NOTATION = "(" + AGE_AD + REGEX_OR + AGE_BC + ")"
AD_BC_OPTIONAL = r"(\s*" + CHRISTUM_NOTATION + ")?"

# -------------------------
# MONTHS
# -------------------------

MONTHS_DIGITS = r"(?:0?[1-9]|10|11|12)"

MONTHS_RO = (
        "("
        + r"ianuarie|fe[bv]ruarie|martie|aprilie|mai|iu[mn]ie|iulie|august|septembrie|[o0]ctombrie|noiembrie|decembrie"
        + REGEX_OR
        + r"(ian|feb(r)?|mart|apr|iun|iul|aug|sept|[o0]ct|noi|dec)\."
        + REGEX_OR
        + r"noimbrie|decembre"
        + ")"
)

MONTHS_EN = (
        "("
        + r"january|february|march|april|may|june|july|august|september|october|november|december"
        + REGEX_OR
        + r"(jan|feb|apr|jun|jul|aug|sep|oct|nov|dec)\."
        + ")"
)

MONTHS = "(" + MONTHS_RO + REGEX_OR + MONTHS_EN + REGEX_OR + MONTHS_DIGITS + ")"

# -------------------------
# AGES NOTATIONS
# -------------------------

AGES_GROUP_SUFFIX = r"([- ]*lea)?"
AGES_ARABIC_GROUP = "(" + TEXT_START + r"\d+" + TEXT_END + ")"

AGES_ARABIC_NOTATION = (
        "("
        + AGES_ARABIC_GROUP
        + AGES_GROUP_SUFFIX
        + "("
        + REGEX_PUNCTUATION_UNLIMITED + CHRISTUM_NOTATION
        + ")?"
        + ")"
)

AGES_ROMAN_GROUP = "(" + TEXT_START + r"[ivxlcdm]+" + TEXT_END + ")"

AGES_ROMAN_NOTATION = (
        "("
        + AGES_ROMAN_GROUP
        + AGES_GROUP_SUFFIX
        + "("
        + REGEX_PUNCTUATION_UNLIMITED + CHRISTUM_NOTATION
        + ")?"
        + ")"
)

AGES_NOTATIONS = "(" + AGES_ROMAN_NOTATION + REGEX_OR + AGES_ARABIC_NOTATION + ")"

# -------------------------
# ARTICLES AND CENTURIES
# -------------------------

ARTICLE_AL = r"(?:al[\.\s]*)?"

START = r"((?:[iî]nceput(?:u(?:l)?|ului)?|[iî]nc\.?)(?:\s+de)?)?"
END = r"((?:sf[aâ]r[sșş]it(?:u(?:l)?)?|sf[\.\s]{0,6})(?:\s+de)?)?"

# E.g.: "sfârșitul sec. xi-începutul sec. xiii p. chr"
START_END = END + START
# TODO: ???
# START_END = f"(?:{START}|{END})"

CENTURY_LABEL = (
        "("
        + START_END
        + r"\s*(?:(secol|secoi)(?:ele|ului|ul)?|sec)[\.\s]*"
        + ARTICLE_AL
        + ")"
)

MILLENNIUM_LABEL = (
        "("
        + START_END
        + r"\s*(?:mileni(?:ile|ului|ul)?|mil)[\.\s]*"
        + ARTICLE_AL
        + ")"
)

YEAR_LABEL = (
        "("
        + START_END
        + r"\s*(?:ani+(?:lor)?|an(?:ului|ulu|ul|u)?)\s*"
        + ARTICLE_AL
        + ")"
)

# -------------------------
# HALF / QUARTERS
# -------------------------

HALF = r"jum([aă]tate(a)?)?"
FIRST_HALF_STRING_REGEX = "(" + r"prim[a]*[\. ]+" + "(" + HALF + r"|part)" + ")"
SECOND_HALF_STRING_REGEX = "(" + r"a\s+(doua|(ii[-a]*))[\. ]+" + "(" + HALF + r"|part)" + ANY_WORDS + ")"

REGEX_A_AL_POSTFIX = "(" + ANY_WORDS + r"[\.]*([\. ]+(a|al))*" + ")"

FIRST_HALF = (
        "("
        + TEXT_START + "("
        + r"(1/2)" + REGEX_OR
        + r"(½)" + REGEX_OR
        + "(" + FIRST_HALF_STRING_REGEX + REGEX_A_AL_POSTFIX + ")"
        + ")" + TEXT_END
        + ")"
)

SECOND_HALF = (
        "("
        + TEXT_START + "("
        + r"(2/2)" + REGEX_OR
        + "(" + SECOND_HALF_STRING_REGEX + REGEX_A_AL_POSTFIX + ")"
        + ")" + TEXT_END
        + ")"
)

MIDDLE_OF = (
        "("
        + TEXT_START + "(" + HALF + r"|(mij" + ANY_WORDS + r")|mj\." + TEXT_END + ")"
        + ")"
)

# -------------------------
# QUARTERS
# -------------------------

FIRST_QUARTER = (
        "("
        + TEXT_START + "("
        + r"(1/4)" + REGEX_OR
        + r"(¼)" + REGEX_OR
        + "(" + r"([iî]nc" + ANY_WORDS + r"[\. ]*)" + r"(de)?" + ")" + REGEX_OR
        + "(" + r"primul\s+sfert" + r"(\s+a[l]?)?" + ")" + REGEX_OR
        + "(" + r"prima treime a" + ")"
        + ")" + TEXT_END
        + ")"
)

SECOND_QUARTER = (
        "("
        + TEXT_START + "("
        + r"(2/4)" + REGEX_OR
        + r"(al doile[a]? sfert al)"
        + ")" + TEXT_END
        + ")"
)

THIRD_QUARTER = (
        "("
        + TEXT_START + "("
        + r"(3/4)" + REGEX_OR
        + r"(¾)" + REGEX_OR
        + r"(al treilea sfert al)"
        + ")" + TEXT_END
        + ")"
)

FORTH_QUARTER = (
        "("
        + TEXT_START + "("
        + r"(4/4)" + REGEX_OR
        + "(" + r"(ultimul\s+sfert)" + r"(\s+(a[l]?|de)*)?" + ")"
        + ")"
        + ")"
)
