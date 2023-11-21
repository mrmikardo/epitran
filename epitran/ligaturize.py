def ligaturize(text):
    """Convert text to employ non-standard ligatures

    Args:
        text (unicode): IPA text to Convert

    Return:
        unicode: non-standard IPA text with phonetic ligatures for affricates
    """
    mapping = [
        ("t͡s", "ʦ"),
        ("t͡ʃ", "ʧ"),
        ("t͡ɕ", "ʨ"),
        ("d͡z", "ʣ"),
        ("d͡ʒ", "ʤ"),
        ("d͡ʑ", "ʥ"),
    ]
    for from_, to_ in mapping:
        text = text.replace(from_, to_)
    return text
