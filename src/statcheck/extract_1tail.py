import re

def extract_1tail(txt):
    """
    Extracts the 1-tailed p-value from a string.
    :param txt: string
    :return: Whether the test is one-tailed
    """
    # search for "one-sided"/"one-tailed"/"directional" in full text to detect one-sided testing
    onesided = re.search("one.?sided|one.?tailed|directional", txt, re.IGNORECASE)

    if onesided:
        onesided = 1
    else:
        onesided = 0

    OneTailedInTxt = bool(onesided)

    return (OneTailedInTxt)