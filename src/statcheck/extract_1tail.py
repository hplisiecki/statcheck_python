import re

def extract_1tail(txt):
    # search for "one-sided"/"one-tailed"/"directional" in full text to detect one-sided testing
    onesided = re.search("one.?sided|one.?tailed|directional", txt, re.IGNORECASE)

    if onesided:
        onesided = 1
    else:
        onesided = 0

    OneTailedInTxt = bool(onesided)

    return (OneTailedInTxt)