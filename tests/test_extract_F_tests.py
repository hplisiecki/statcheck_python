import os
import sys
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from statcheck import statcheck

# test if the following p-values are correctly retrieved ----------------------

# standard F-tests
def test_F1():
    txt1 = "F(2, 28) = 2.20, p = .03"
    Res, pRes = statcheck(txt1)
    assert len(Res) == 1, "Length of Res is not 1"
    assert Res['Statistic'].iloc[0] == 'F', "Statistic is not F"
    assert Res['df1'].iloc[0] == 2.0, "df1 is not 2.0"
    assert Res['df2'].iloc[0] == 28, "df2 is not 28"
    assert Res['Test_Comparison'].iloc[0] == '=', "Test_Comparison is not ="
    assert Res['Value'].iloc[0] == 2.2, "Test_Value is not 2.2"
    assert Res['Reported_P_Comparison'].iloc[0] == "=", "Reported_Comparison is not ="
    assert Res['Reported_P_Value'].iloc[0] == 0.03, "Reported_p is not .03"
    assert Res['Raw'].iloc[0] == "F(2, 28) = 2.20, p = .03", "Raw is not F(2, 28) = 2.20, p = .03"

# standard F-tests in text
def test_F2():
    txt1 = "The effect was very significant, F(2, 28) = 2.20, p = .03."
    txt2 = "Both effects were very significant, F(2, 28) = 2.20, p = .03, F(2, 28) = 1.23, p = .04."

    Res, pRes = statcheck([txt1, txt2])
    assert len(pRes) == 3, "Length of Res is not 3"
    assert list(Res['Source'].values) == [0, 1, 1], "source is not [0, 1, 1]"

# variation in spacing
def test_F3():
    txt1 = " F ( 2 , 28 ) = 2.20 , p = .03"
    txt2 = "F(2,28)=2.20,p=.03"
    Res, pRes = statcheck([txt1, txt2])
    assert len(Res) == 2, "Length of Res is not 2"

# variations in the degrees of freedom
def test_F4():
    txt1 = "F(2.1, 28.1) = 2.20, p = .03"
    txt2 = "F(l, 76) = 23.95, p <.001"  # this wrong notation happens occasionally in articles

    Res, pRes = statcheck([txt1, txt2])

    assert len(Res) == 2, "Length of Res is not 2"
    assert list(Res['df1'].values) == [2.1, 1.0], "df1 is not [2.1, 1.0]"
    assert list(Res['df2'].values) == [28.1, 76.0], "df2 is not [28.1, 76.0]"







