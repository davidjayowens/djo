import unicodedata


def normalize_text(text):
    """
    NFKD form: "Normalization Form Compatibility Decomposition"

    Improves text matching by removing character accents/decorators, 
    reducing each letter to its base form (so 'é' -> 'e', etc).

    Note that this may result in some non-normalizeable characters
    being removed from the final text.
    """

    try:
        nfkd_form = unicodedata.normalize('NFKD', text)
        only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('utf-8', 'ignore')

        return(only_ascii)
    except:
        return(None)