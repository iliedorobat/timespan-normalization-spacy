from validation import validate_ronec_corpus, validate_inp_data

if __name__ == "__main__":
    validate_ronec_corpus("validation")
    validate_ronec_corpus("test")

    # TODO: WIP:
    # validate_inp_data("additional")
    # validate_inp_data("all")
    # validate_inp_data("unique")
