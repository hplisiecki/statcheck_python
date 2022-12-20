import sys
import os
import pandas as pd
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from statcheck import statcheck

# test if the following z-tests are correctly retrieved ----------------------

# standard z-tests
def test_z1():
    txt1 = " z = 2.20, p = .03"
    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['Statistic'].iloc[0] == 'Z', "Statistic is not Z"
    assert pd.isna(Res['df1'].iloc[0]), "df1 is not NA"
    assert pd.isna(Res['df2'].iloc[0]), "df2 is not NA"
    assert Res['Test_Comparison'].iloc[0] == '=', "Test_Comparison is not ="
    assert Res['Value'].iloc[0] == 2.20, "Test_Value is not 2.20"
    assert Res['Reported_P_Comparison'].iloc[0] == "=", "Reported_Comparison is not ="
    assert Res['Reported_P_Value'].iloc[0] == 0.03, "Reported_p is not .03"
    assert Res['Raw'].iloc[0] == "z = 2.20, p = .03", "Raw is not z = 2.20, p = .03"

# standard z-tests in text
def test_z2():
    txt1 = "The effect was very significant, z = 2.20, p = .03."
    txt2 = "Both effects were very significant, z = 2.20, p = .03, z = 1.23, p = .04."
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 3, "Length of Res is not 3"
    assert list(Res['Source'].values) == [0, 1, 1], "source is not [0, 1, 1]"


# variation in spacing
def test_z3():
    txt1 = " z = 2.20 , p = .03"
    txt2 = " z=2.20,p=.03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"


# variation in capitalization
def test_z4():
    txt = " Z = 2.20 , p = .03"
    Res, pRes = statcheck(txt)
    assert len(Res) == 1, "Length of Res is not 1"


# test if the following incorrect z-tests are not retrieved --------------------

# z test cannot have df
def test_z5():
    txt1 = " z(28) = 2.20, p = .03"
    txt2 = " Z(28) = 2.20, p = .03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 0, "Length of Res is not 0"