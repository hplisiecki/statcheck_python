import sys
import os
from scipy.stats import t
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from st import statcheck


# python tests for error

########################################################
########################################################
# Test 1
# test if the following cases are correctly identified as errors --------------
# check classification of regular errors in all types of tests

def test1():
    txt1 = "t(28) = 2.20, p = .03"
    txt2 = "F(2, 28) = 2.20, p = .15"
    txt3 = "r(28) = .22, p = .26"
    txt4 = "chi2(28) = 22.20, p = .79"
    txt5 = " z = 2.20, p = .04"
    txt6 = "Q(28) = 22.20, p = .79"
    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt6])
    assert list(Res["Error"].values) == [True, True, True, True, True, True], "Test 1 failed"


########################################################
########################################################
# Test 2
# classify inexactly reported p-values correctly

def test2():
    txt1 = "t(28) = 2.20, ns"
    txt2 = "t(28) = 2.20, p > .05"
    txt3 = "t(28) = 2.0, p < .05"
    Res, pRes = statcheck([txt1, txt2, txt3])
    assert list(Res["Error"].values) == [True, True, False], "test2 failed"


########################################################
########################################################
# Test 3
# also classify decision errors as errors

def test3():
    txt1 = "t(28) = 1.20, p = .03"
    txt2 = "t(28) = 2.20, p = .30"
    Res, pRes = statcheck([txt1, txt2])
    assert list(Res["Error"].values) == [True, True], "Test 3 failed"


########################################################
########################################################
# Test 4
# test if the following cases are correctly identified as correct -------------

# correct rounding
def test4():
    txt1 = "t(28) = 2, p = .02"
    txt2 = "t(28) = 2, p = .14"
    txt3 = "t(28) = 2.2, p = .03"  # rounded lower bound p-value
    txt4 = "t(28) = 2.2, p = .04"
    txt5 = "t(28) = 2.20, p = .036"
    txt6 = "t(28) = 2.20, p = .037"
    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt6])
    assert list(Res["Error"].values) == [False, False, False, False, False, False], "test4 failed"

########################################################
########################################################
# Test 5
# test if different arguments concerning errors work --------------------------

# OneTailedTests: assume all tests are one-tailed
def test5():
    txt1 = "t(28) = 2.20, p = .02"
    txt2 = "t(28) = 2.20, p = .04"
    txt3 = "this test is one-tailed: t(28) = 2.20, p = .02, but this one is not: t(28) = 2.20, p = .04"
    Res, pRes = statcheck([txt1, txt2, txt3], OneTailedTests = True)
    assert list(Res["Error"].values) == [False, True, False, True], "Test 5 failed"


########################################################
########################################################
# Test 6
# OneTailedTxt: automated detection of one-tailed test in text
def test6():
    txt1 = "t(28) = 2.20, p = .018"
    txt2 = "t(28) = 2.20, p = .01, one-tailed"
    txt3 = "t(28) = 2.20, p = .018, one-tailed"
    txt4 = "t(28) = 2.20, p = .018, one-sided"
    txt5 = "t(28) = 2.20, p = .018, directional"
    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5], OneTailedTxt = True)
    assert list(Res["Error"].values) == [True, True, False, False, False], "test 6 failed"

########################################################
########################################################
# Test 7
# pZeroError: check if p = .000 is counted as an inconsistency or not

def test7():
    txt1 = "t(28) = 22.20, p = .000"
    txt2 = "t(28) = 22.20, p < .000"
    Res, pRes = statcheck([txt1, txt2])
    assert list(Res["Error"].values) == [True, True], "Test 7a failed"
    Res, pRes = statcheck([txt1, txt2], pZeroError = False)
    assert list(Res["Error"].values) == [False, True], "Test 7b failed"


########################################################
########################################################
# Test 8
# test classifications of (in)exact test statistcs and (in)exact p-values ----

# test statistics exactly reported
def test8():
    # calculate range of correct p-values
    lowp = (1 - t.cdf(2.25, 28))*2
    upp = (1 - t.cdf(2.15, 28))*2

    # correct
    txt1 = "t(28) = 2.2, p = .036"  # correct
    txt2 = "t(28) = 2.2, p < .08"  # correct
    txt3 = "t(28) = 2.2, p > .02"  # correct

    # error
    txt4 = "t(28) = 2.2, p > " + str(upp)  # error
    txt5 = "t(28) = 2.2, p < " + str(lowp)  # error

    txt6 = "t(28) = 2.2, p = .08"  # error
    txt7 = "t(28) = 2.2, p = .02"  # error
    txt8 = "t(28) = 2.2, p > .08"  # error
    txt9 = "t(28) = 2.2, p < .02"  # error

    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9])
    assert list(Res["Error"].values) == [False, False, False, True, True, True, True, True, True], "test8 failed"


########################################################
########################################################
# Test 9
# test statistic reported as <

def test9():
    # calculate range of correct p-values
    lowp = (1 - t.cdf(2.25, 28))*2
    upp = (1 - t.cdf(2.15, 28))*2

    # correct
    txt1 = "t(28) < 2.20, p > " + str(upp)
    txt2 = "t(28) < 2.2, p = .08"
    txt3 = "t(28) < 2.2, p > .08"
    txt4 = "t(28) < 2.2, p < .08"
    txt5 = "t(28) < 2.2, p > .02"

    # error
    txt6 = "t(28) < 2.2, p = " + str(lowp)
    txt7 = "t(28) < 2.2, p < " + str(lowp) # fail
    txt8 = "t(28) < 2.2, p < .02" # fail
    txt9 = "t(28) < 2.2, p = .02"

    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt6, txt9])
    assert list(Res["Error"].values) == [False, False, False, False, False, True, True], "test9 failed"

    Res, pRes = statcheck([txt7, txt8])
    assert list(Res["Error"].values) == [True, True], "test9 commented out in the original, failed"


########################################################
########################################################
# Test 10
# test statistic reported as >

def test10():
    # calculate range of correct p-values
    upp = (1 - t.cdf(2.15, 28))*2

    # correct
    txt1 = "t(28) > 2.20, p < " + str(upp)
    txt2 = "t(28) > 2.2, p = .02"
    txt3 = "t(28) > 2.2, p > .02"
    txt4 = "t(28) > 2.2, p < .02"
    txt5 = "t(28) > 2.2, p < .08"

    # error
    txt6 = "t(28) > 2.2, p = " + str(upp) # fail
    txt7 = "t(28) > 2.2, p > " + str(upp) # fail
    txt8 = "t(28) > 2.2, p > .08" # fail
    txt9 = "t(28) > 2.2, p = .08"

    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt9])
    assert list(Res["Error"].values) == [False, False, False, False, False, True], "test10 failed"

    Res, pRes = statcheck([txt6, txt7, txt8]) # commented out in the original
    assert list(Res["Error"].values) == [True, True, True], "test10 commented out in the original failed"

