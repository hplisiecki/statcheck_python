import os
import sys
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from st import statcheck
import pandas as pd

# test if the following p-values are correctly retrieved ----------------------

# standard correlation
def testCorr1():
    txt1 = "r(28) = .20, p = .03"
    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['Statistic'].iloc[0] == 'r', "Statistic is not r"
    assert pd.isna(Res['df1'].iloc[0]), "df1 is not NA"
    assert Res['df2'].iloc[0] == 28, "df2 is not 28"
    assert Res['Test_Comparison'].iloc[0] == '=', "Test_Comparison is not ="
    assert Res['Value'].iloc[0] == .2, "Test_Value is not .2"
    assert Res['Reported_P_Comparison'].iloc[0] == "=", "Reported_Comparison is not ="
    assert Res['Reported_P_Value'].iloc[0] == 0.03, "Reported_p is not .03"
    assert Res['Raw'].iloc[0] == "r(28) = .20, p = .03", "Raw is not r(28) = .20, p = .03"

# standard correlations in text
def testCorr2():
    txt1 = "The effect was very significant, r(28) = .20, p = .03."
    txt2 = "Both effects were very significant, r(28) = .20, p = .03, r(28) = .23, p = .04."
    Res, pRes = statcheck([txt1, txt2])
    assert len(pRes) == 3, "Length of Res is not 3"
    assert list(Res['Source'].values) == [0, 1, 1], "source is not [0, 1, 1]"

# variation in spacing
def testCorr3():
    txt1 = " r ( 28 ) = .20 , p = .03"
    txt2 = "r(28)=.20,p=.03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"

# test if the following incorrect correlations are not retrieved ------------------

# do not extract correlations larger than 1 or smaller than -1
def testCorr4():
    txt1 = "r(16) = 26.05, p = .10"
    txt2 = "r(28) = −59, p = .0008"

    Res, pRes = statcheck([txt1, txt2])

    assert len(Res) == 0, "Length of Res is not 0"







