from temporal_normalization.rules.timespan_regex import (
    ANY_WORDS,
    TEXT_END,
    TEXT_START,
)

"""
Regular expressions for those time intervals that point to
an age (epoch) time period
"""

# <a href="http://dbpedia.org/page/Pleistocene">Pleistocene</a>
PLEISTOCENE_AGE = TEXT_START + r"(pleistocen)" + TEXT_END

# <a href="http://dbpedia.org/page/Mesolithic">Mesolithic</a>
MESOLITHIC_AGE = TEXT_START + r"(epipaleolitic)" + TEXT_END

# <a href="http://dbpedia.org/page/Chalcolithic">Chalcolithic</a>
CHALCOLITHIC_AGE = TEXT_START + r"(eneolitic)" + TEXT_END

# <a href="http://dbpedia.org/page/Neolithic">Neolithic</a>
NEOLITHIC_AGE = TEXT_START + r"(neolitic" + ANY_WORDS + r")" + TEXT_END

# <a href="http://dbpedia.org/page/Bronze_Age">Bronze_Age</a>
BRONZE_AGE = TEXT_START + r"(bronz|bronzului|tarzii)" + TEXT_END

# <a href="http://dbpedia.org/page/Aurignacian">Aurignacian</a>
AURIGNACIAN_CULTURE = TEXT_START + r"(aurignacian)" + TEXT_END

# <a href="http://dbpedia.org/page/Hallstatt_culture">Hallstatt Culture</a>
HALLSTATT_CULTURE = TEXT_START + r"(hallstatt)" + TEXT_END

# <a href="http://dbpedia.org/page/Middle_Ages">Middle Ages</a>
MIDDLE_AGES = TEXT_START + r"(medieval|medievala)" + TEXT_END

# <a href="http://dbpedia.org/page/Modern_history">Modern History</a>
MODERN_AGES = TEXT_START + r"(moderna)" + TEXT_END

# <a href="http://dbpedia.org/page/Ptolemaic_dynasty">Ptolemaic Dynasty</a>
PTOLEMAIC_DYNASTY = TEXT_START + r"(ptolem" + ANY_WORDS + r")" + TEXT_END

# <a href="http://dbpedia.org/page/Roman_Empire">Roman Empire</a>
ROMAN_EMPIRE_AGE = TEXT_START + r"(romana)" + TEXT_END

# <a href="http://dbpedia.org/page/Nerva">Nerva–Antonine Dynasty</a>
NERVA_ANTONINE_DYNASTY = TEXT_START + r"(antoninian" + ANY_WORDS + r"|hadrian)" + TEXT_END

# <a href="http://dbpedia.org/page/Renaissance">Renaissance</a>
RENAISSANCE = TEXT_START + r"(renastere)" + TEXT_END

# <a href="http://dbpedia.org/page/French_Consulate">French Consulate</a>
FRENCH_CONSULATE_AGE = TEXT_START + r"(perioada consulatului francez)" + TEXT_END

# <a href="http://dbpedia.org/page/World_War_I">World War I</a>
WW_I_PERIOD = TEXT_START + r"(primul razboi mondial)" + TEXT_END

# <a href="http://dbpedia.org/page/Interwar_period">Interwar Period</a>
INTERWAR_PERIOD = TEXT_START + r"(interbelica)" + TEXT_END

# <a href="http://dbpedia.org/page/World_War_II">World War II</a>
WW_II_PERIOD = TEXT_START + r"(al (doilea|ii-lea) razboi mondial)" + TEXT_END


AGE_OPTIONS = [
    PLEISTOCENE_AGE,
    MESOLITHIC_AGE,
    CHALCOLITHIC_AGE,
    NEOLITHIC_AGE,
    BRONZE_AGE,
    MIDDLE_AGES,
    MODERN_AGES,
    HALLSTATT_CULTURE,
    AURIGNACIAN_CULTURE,
    PTOLEMAIC_DYNASTY,
    ROMAN_EMPIRE_AGE,
    NERVA_ANTONINE_DYNASTY,
    RENAISSANCE,
    FRENCH_CONSULATE_AGE,
    WW_I_PERIOD,
    INTERWAR_PERIOD,
    WW_II_PERIOD,
]


AGE_REGEXES = [
    AURIGNACIAN_CULTURE,
    BRONZE_AGE,
    CHALCOLITHIC_AGE,
    FRENCH_CONSULATE_AGE,
    HALLSTATT_CULTURE,
    INTERWAR_PERIOD,
    MESOLITHIC_AGE,
    MIDDLE_AGES,
    MODERN_AGES,
    NEOLITHIC_AGE,
    NERVA_ANTONINE_DYNASTY,
    PLEISTOCENE_AGE,
    PTOLEMAIC_DYNASTY,
    RENAISSANCE,
    ROMAN_EMPIRE_AGE,
    WW_I_PERIOD,
    WW_II_PERIOD,
]
