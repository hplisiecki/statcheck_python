import os
import sys
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from statcheck import statcheck
import pandas as pd

# test if the following p-values are correctly retrieved ----------------------

# standard p-values
def test_p1():
    txt1 = "p = .05"
    txt2 = "p < .05"
    txt3 = "p > .05"

    Res, pRes = statcheck([txt1, txt2, txt3])
    assert len(pRes) == 3, "Length of Res is not 3"
    assert list(pRes['Reported_P_Comparison'].values) == ["=", "<", ">"], "Comparisons are not =, <, >"
    assert list(pRes['Reported_P_Value'].values) == [0.05, 0.05, 0.05], "p-values are not 0.05" # error in original

# non-significant results
def test_p2():
    txt1 = "the result was not significant, ns"

    Res, pRes = statcheck(txt1)
    assert len(pRes) == 1, "Length of Res is not 1"
    assert pRes['Reported_P_Comparison'].iloc[0] == "ns", "Comparison is not ns"
    assert pd.isna(pRes['Reported_P_Value'].iloc[0]), "p-value is not NA"


# test if the following non p-values are not retrieved ------------------

# page number

def test_p3():
    txt1 = "see p. 01"

    Res, pRes = statcheck(txt1)
    assert len(Res) == 0, "Length of Res is not 0"




