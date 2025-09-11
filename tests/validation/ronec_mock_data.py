class DotDict:
    def __init__(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, DotDict(value))
            else:
                setattr(self, key, value)


class FeatureWrapper:
    def __init__(self, data: dict):
        # E.g.: {"feature": {"names": [...]}}
        self.feature = DotDict(data["feature"])


class FeaturesWrapper:
    def __init__(self, data: dict):
        # E.g.: {"ner_tags": {"feature": {"names": [...]}}}
        self._data = {key: FeatureWrapper(value) for key, value in data.items()}

    def __getitem__(self, key):
        return self._data[key]


class ValidationWrapper:
    def __init__(self, data: dict, arr=None):
        # data contains the key "features"
        self.features = FeaturesWrapper(data["features"])
        self._list = arr or []

    def __getitem__(self, key):
        if isinstance(key, int):
            # numeric index -> element in the list
            return self._list[key]
        else:
            # otherwise, if the key is a string, returns the attribute
            if key == "features":
                return self.features
            raise KeyError(f"Key {key} not found")

    def __len__(self):
        return len(self._list)

    def __repr__(self):
        return f"<ValidationWrapper features={self.features} list={self._list}>"


class RonecRoot:
    def __init__(self, data: dict, arr):
        # presupunem că data["validation"] e dict cu "features"
        # și vrem și o listă (exemplu)
        self._data = {"validation": ValidationWrapper(data["validation"], arr)}

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return f"<RonecRoot {self._data}>"


# fmt: off
# test => i = 21
example_1 = {
    "id": 4023,
    "tokens": [
        "După", "finalizarea", "lucrărilor", "la", "linia", "101", ",", "a", "fost", "construit", "și", "Depoul", "de", "Tramvaie", "de", "la", "capătul", "străzii", "Industriei", ",", "cu", "halele", "de", "reparații", "și", "întreținere", ".", "Între", "2004", "și", "2008", ",", "tramvaiele", "sunt", "desființate", "din", "motive", "ideologice", ":", "în", "măsura", "în", "care", "primăria", "condusă", "de", "Radu", "Mazăre", "considera", "că", "transportul", "urban", "pe", "șine", "este", "arhaic", "și", "că", "modernismul", "înseamnă", "să", "se", "dea", "prioritate", "traficului", "de", "automobile", "private", "(", "o", "ideologie", "a", "transportului", "care", "a", "dominat", "Statele-Unite", "și", "Europa", "occidentală", "în", "deceniile", "1950-1970", ")", "tramvaiele", "au", "fost", "socotite", "ca", "o", "cauză", "de", "congestionare", "a", "traficului", "și", "desființate", "conform", "programului", "denumit", "„", "de", "reabilitare", "a", "transportului", "public", "”", ".",  # noqa: E501
    ],
    "ner_ids": [
        0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 19, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 7, 8, 0, 19, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # noqa: E501
    ],
    "space_after": [
        True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, False, False, True, True, True, False, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, False, False,  # noqa: E501
    ],
    "ner_tags": [
        0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 19, 20, 20, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 7, 8, 0, 19, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # noqa: E501
    ],
}

# validation => id = 380
example_2 = {
    "id": 11606,
    "ner_ids": [
        0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 5, 0, 0,  # noqa: E501
    ],
    "ner_tags": [
        0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 5, 0, 0,  # noqa: E501
    ],
    "space_after": [
        True, True, True, True, False, True, False, True, True, True, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, True, True, False, False, False,  # noqa: E501
    ],
    "tokens": [
        "Cu", "ajutorul", "unei", "motocicliste", "curiere", ",", "Mari", ",", "pe", "care", "au", "întâlnit", "-o", "în", "Odaiba", ",", "Mirai", "și", "Yuuki", "se", "luptă", "să", "ajungă", "înapoi", "la", "casa", "lor", ",", "Setagaya", ",", "din", "vestul", "Tokyo", "-ului", ".",  # noqa: E501
    ],
}

ronec_example = RonecRoot(
    {
        "validation": {
            "features": {
                "ner_tags": {
                    "feature": {
                        "names": [
                            "O",
                            "B-PERSON",
                            "I-PERSON",
                            "B-ORG",
                            "I-ORG",
                            "B-GPE",
                            "I-GPE",
                            "B-LOC",
                            "I-LOC",
                            "B-NAT_REL_POL",
                            "I-NAT_REL_POL",
                            "B-EVENT",
                            "I-EVENT",
                            "B-LANGUAGE",
                            "I-LANGUAGE",
                            "B-WORK_OF_ART",
                            "I-WORK_OF_ART",
                            "B-DATETIME",
                            "I-DATETIME",
                            "B-PERIOD",
                            "I-PERIOD",
                            "B-MONEY",
                            "I-MONEY",
                            "B-QUANTITY",
                            "I-QUANTITY",
                            "B-NUMERIC",
                            "I-NUMERIC",
                            "B-ORDINAL",
                            "I-ORDINAL",
                            "B-FACILITY",
                            "I-FACILITY",
                        ]
                    }
                }
            }
        }
    },
    [example_1, example_2],
)
# fmt: on

if __name__ == "__main__":
    test = ronec_example["validation"].features["ner_tags"].feature.names
