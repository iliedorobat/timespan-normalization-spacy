from datetime import datetime

from langdetect import detect


# https://godoc.org/github.com/whitedevops/colors
class COLORS:
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    LIGHT_CYAN = "\033[96m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_RED = "\033[91m"
    RED = "\033[31m"
    RESET_ALL = "\033[0m"


# https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python#answer-287944
class console:
    @staticmethod
    def display(message: str, color: str, alert: str, show_time: bool = True):
        if show_time:
            print(
                f"{color}{datetime.now().replace(microsecond=0)} {alert}: {message}{COLORS.RESET_ALL}"  # noqa 501
            )
        else:
            print(f"{color}{message}{COLORS.RESET_ALL}")

    @staticmethod
    def debug(message: str, show_time: bool = True):
        console.display(message, COLORS.CYAN, "DEBUG", show_time)

    @staticmethod
    def log(message: str, show_time: bool = True):
        console.display(message, COLORS.BLUE, "LOG", show_time)

    @staticmethod
    def info(message: str, show_time: bool = True):
        console.display(message, COLORS.LIGHT_CYAN, "INFO", show_time)

    @staticmethod
    def warning(message: str, show_time: bool = True):
        console.display(message, COLORS.LIGHT_YELLOW, "WARNING", show_time)

    @staticmethod
    def error(message: str, show_time: bool = True):
        console.display(message, COLORS.RED, "ERROR", show_time)

    @staticmethod
    def lang_warning(query: str, target_lang: str):
        if detect(query) != target_lang:
            console.warning(
                f'Detected language: "{detect(query)}" but required: "{target_lang}"'
            )

    @staticmethod
    def tokens_table(document):
        console.info(
            f"-------------------------------------------------------------------------------------------------------"
            f'\n{"Token":{15}}|{"Lemma":{15}}|{"POS":{10}}|{"TAG":{10}}|'
            f'{"DEP":{10}}|{"shape_":{15}}|{"is_alpha":{10}}',
            show_time=False,
        )
        console.info(
            "-------------------------------------------------------------------------------------------------------",
            show_time=False,
        )
        for token in document:
            console.info(
                f"{token.text:{15}}|{token.lemma_:{15}}|{token.pos_:{10}}|{token.tag_:{10}}|{token.dep_:{10}}|"
                f"{token.shape_:{15}}|{token.is_alpha:{10}}",
                show_time=False,
            )
        console.info(
            "-------------------------------------------------------------------------------------------------------",
            show_time=False,
        )
        console.info(f"sentence: {document}", show_time=False)

    @staticmethod
    def deps_list(document):
        separator = ""
        for i in range(130):
            separator += "-"

        console.info(
            f"{separator}\n"
            f"  "
            f'{"Token":{15}}|{"Governor":{10}}|{"Root Node":{10}}|'
            f'{"Lefts":{20}}|{"Rights":{20}}|'
            f'{"Lemma":{15}}|{"POS":{10}}|{"TAG":{10}}|{"DEP":{10}}'
        )
        console.info(separator)
        for token in document:
            console.info(
                f"  "
                f"{token.text:{15}}|{token.head.text:{10}}|{str(token == token.head):{10}}|"  # noqa 501
                f"{str(list(token.lefts)):{20}}|{str(list(token.rights)):{20}}|"
                f"{token.lemma_:{15}}|{token.pos_:{10}}|{token.tag_:{10}}|{token.dep_:{10}}"
            )
        console.info(separator)
        console.info(f"sentence: {document}")
