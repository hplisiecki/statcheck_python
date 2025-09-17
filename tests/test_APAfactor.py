import sys
import os
from statcheck.st import statcheck

# python tests for the APA factor

# Test variables
txt1 = "This text has 50% of its stats in APA style: t(28) = 2.20, p < .05, some other p = .035."
txt2 = "This text has 100% of its stats in APA style: t(28) = 2.20, p < .05."

result1 = .5
result2 = 1
result12 = [.5, 1]

# test 1
def test_APAfactor1():
    Res, pRes = statcheck(txt1)
    assert Res['APAfactor'].iloc[0] == result1

# test 2
def test_APAfactor2():
    Res, pRes = statcheck(txt2)
    assert Res['APAfactor'].iloc[0] == result2, "Test 2 failed"

# test 3
def test_APAfactor3():
    Res, pRes = statcheck([txt1, txt2])
    assert list(Res['APAfactor'].values) == result12, "Test 3 failed"
