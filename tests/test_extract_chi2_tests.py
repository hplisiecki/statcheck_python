import sys
import os
from statcheck.st import statcheck
import pandas as pd

# test if the following Q-tests are correctly retrieved ----------------------

# standard chi2-test
def test_chi1():
    txt1 = "chi2(28) = 2.20, p = .03"
    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['Statistic'].iloc[0] == 'Chi2', "Statistic is not Chi2"
    assert Res['df1'].iloc[0] == 28, "df1 is not 28"
    assert pd.isna(Res['df2'].iloc[0]), "df2 is not NA"
    assert Res['Test_Comparison'].iloc[0] == '=', "Test_Comparison is not ="
    assert Res['Value'].iloc[0] == 2.20, "Test_Value is not 2.20"
    assert Res['Reported_P_Comparison'].iloc[0] == "=", "Reported_Comparison is not ="
    assert Res['Reported_P_Value'].iloc[0] == 0.03, "Reported_p is not .03"
    assert Res['Raw'].iloc[0] == "i2(28) = 2.20, p = .03", "i2(28) = 2.20, p = .03"

# standard chi2-tests in text
def test_chi2():
    txt1 = "The effect was very significant, chi2(28) = 2.20, p = .03."
    txt2 = "Both effects were very significant, chi2(28) = 2.20, p = .03, chi2(28) = 1.23, p = .04."
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 3, "Length of Res is not 3"
    assert list(Res['Source'].values) == [0, 1, 1], "source is not [0, 1, 1]"

# variations in extracted "chi2"
def test_chi3():
    txt1 = "X2(28) = 2.20, p = .03"
    txt2 = "x2(28) = 2.20, p = .03"
    txt3 = "chi_2(28) = 2.20, p = .03"

    Res, pRes = statcheck([txt1, txt2, txt3])
    assert len(Res) == 3, "Length of Res is not 3"


# variation in degrees of freedom
def test_chi4():
    txt1 = "chi2(28, N = 129) = 2.2, p = .03"
    txt2 = "chi2(1, N = 11,455) = 16.78, p <.001"

    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"

# variation in spacing
def test_chi5():
    txt1 = " chi2 ( 28 ) = 2.20 , p = .03"
    txt2 = "chi2(28)=2.20,p=.03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"