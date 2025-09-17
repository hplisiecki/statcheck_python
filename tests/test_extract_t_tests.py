import sys
import os
from statcheck.st import statcheck
import pandas as pd

# print the files



# test if the following t-tests are correctly retrieved ----------------------

# standard t-test
def test_t1():
    txt1 = "t(28) = 2.20, p = .03"
    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['Statistic'].iloc[0] == 't', "Statistic is not t"
    assert pd.isna(Res['df1'].iloc[0]), "df1 is not NA"
    assert Res['df2'].iloc[0] == 28, "df2 is not 28"
    assert Res['Test_Comparison'].iloc[0] == '=', "Test_Comparison is not ="
    assert Res['Value'].iloc[0] == 2.20, "Test_Value is not 2.20"
    assert Res['Reported_P_Comparison'].iloc[0] == "=", "Reported_Comparison is not ="
    assert Res['Reported_P_Value'].iloc[0] == 0.03, "Reported_p is not .03"
    assert Res['Raw'].iloc[0] == "t(28) = 2.20, p = .03", "Raw is not t = 2.20, p = .03"

# standard t-tests in text
def test_t2():
    txt1 = "The effect was very significant, t(28) = 2.20, p = .03."
    txt2 = "Both effects were very significant, t(28) = 2.20, p = .03, t(28) = 1.23, p = .04."
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 3, "Length of Res is not 3"
    assert list(Res['Source'].values) == [0, 1, 1], "source is not [0, 1, 1]"


# variation in spacing
def test_t3():
    txt1 = " t ( 28 ) = 2.20 , p = .03"
    txt2 = "t(28)=2.20,p=.03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"

# variations test statistic
def test_t4():
    txt1 = "t(28) = -2.20, p = .03"
    txt2 = "t(28) = 2,000.20, p = .03"
    txt3 = "t(28) < 2.20, p = .03"
    txt4 = "t(28) > 2.20, p = .03"
    txt5 = "t(28) = %^&2.20, p = .03"  # read as -2.20

    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5])
    assert len(Res) == 5, "Length of Res is not 5"

# variation p-value
def test_t5():
    txt1 = "t(28) = 2.20, p = 0.03"
    txt2 = "t(28) = 2.20, p < .03"
    txt3 = "t(28) = 2.20, p > .03"
    txt4 = "t(28) = 2.20, ns"
    txt5 = "t(28) = 2.20, p = .5e-3"

    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5])
    assert len(Res) == 5, "Length of Res is not 5"


# corrected degrees of freedom
def test_t6():
    txt1 = "t(28.1) = 2.20, p = .03"

    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['df2'].iloc[0] == 28.1, "df2 is not 28.1"

# test if the following incorrect z-tests are not retrieved --------------------

# test if the following incorrect t-tests are not retrieved ------------------

# punctuation
def test_t7():
    txt1 = "t(28) = 2.20; p = .03"
    txt2 = "t[28] = 2.20, p = .03"
    txt3 = "t(28) = .2.20, p = .03"

    Res, pRes = statcheck([txt1, txt2, txt3])
    assert len(Res) == 0, "Length of Res is not 0"


def test_t8():
    txt1 = "T(28) = 2.20, p = .03"

    Res, pRes = statcheck(txt1)
    assert len(Res) == 0, "Length of Res is not 0"

# not a p-value
def test_t9():
    txt1 = "t(28) = 2.20, p = 1.03"

    Res, pRes = statcheck(txt1)
    assert len(Res) == 0, "Length of Res is not 0"

# wrong df
def test_t10():
    txt1 = "t(2,28) = 2.20, p = .03"

    Res, pRes = statcheck(txt1)
    assert len(Res) == 0, "Length of Res is not 0"

# weird encoding in minus sign followed by space
def test_t11():
    txt1 = " t(553) = − 4.46, p < .0001" # this is an em dash or something

    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1" # original error has been fixed

