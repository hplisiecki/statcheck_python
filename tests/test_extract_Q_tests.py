import sys
import os
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from statcheck import statcheck
import pandas as pd



# test if the following Q-tests are correctly retrieved ----------------------

# standard Q-test
def test_Q1():
    txt1 = "Q(2) = 2.20, p = .03"
    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['Statistic'].iloc[0] == 'Q', "Statistic is not Q"
    assert Res['df1'].iloc[0] == 2.0, "df1 is not 2.0"
    assert pd.isna(Res['df2'].iloc[0]), "df2 is not NA"
    assert Res['Test_Comparison'].iloc[0] == '=', "Test_Comparison is not ="
    assert Res['Value'].iloc[0] == 2.20, "Test_Value is not 2.20"
    assert Res['Reported_P_Comparison'].iloc[0] == "=", "Reported_Comparison is not ="
    assert Res['Reported_P_Value'].iloc[0] == 0.03, "Reported_p is not .03"
    assert Res['Raw'].iloc[0] == "Q(2) = 2.20, p = .03", "Raw is not Q(2) = 2.20, p = .03"

# standard Q-tests in text
def test_Q2():
    txt1 = "The effect was very significant, Q(2) = 2.20, p = .03."
    txt2 = "Both effects were very significant, Q(2) = 2.20, p = .03, Q(2) = 1.23, p = .04."
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 3, "Length of Res is not 3"
    assert list(Res['Source'].values) == [0, 1, 1], "source is not [0, 1, 1]"


# variation in spacing
def test_Q3():
    txt1 = " Q ( 2 ) = 2.20 , p = .03"
    txt2 = "Q(2)=2.20,p=.03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"

# variations test statistic
def test_Q4():
    txt1 = "Qw(2) = 2.20, p = .03"
    txt2 = "Qwithin(2) = 2.20, p = .03"
    txt3 = "Q-within(2) = 2.20, p = .03"
    txt4 = "Qb(2) = 2.20, p = .03"
    txt5 = "Qbetween(2) = 2.20, p = .03"
    txt6 = "Q-between(2) = 2.20, p = .03"

    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt6])
    assert len(Res) == 6, "Length of Res is not 5"

# test if the following 'incorrect' Q-tests are not retrieved ----------------
def test_Q5():
    txt1 = "Qs(2) = 2.2, p = .03"
    txt2 = "Qb(2, N = 187) = 2.20, p = .03"

    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 0, "Length of Res is not 0"