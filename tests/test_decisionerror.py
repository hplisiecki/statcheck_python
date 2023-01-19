import sys
import os
from scipy.stats import t
src_dir = os.path.abspath(os.path.join(__file__, "../../src/statcheck"))
sys.path.insert(0, src_dir)
from st import statcheck

# python tests for the decision error

########################################################
########################################################
# Test 1 variables
# test if the following cases are correctly identified as decision errors -----
# check classification of regular decision errors in all types of tests

# Test 1
def test_all():
    txt1 = "t(28) = 2.20, p = .06"
    txt2 = "t(28) = 1.20, p = .03"
    txt3 = "F(2, 28) = 22.20, p = .06"
    txt4 = "F(2, 28) = 2.20, p = .03"
    txt5 = "r(28) = .22, p = .03"
    txt6 = "r(28) = .52, p = .06"
    txt7 = "chi2(28) = 2.20, p = .03"
    txt8 = "chi2(28) = 52.20, p = .06"
    txt9 = " z = 1.20, p = .03"
    txt10 = " z = 2.20, p = .06"
    txt11 = "Q(28) = 2.20, p = .03"
    txt12 = "Q(28) = 52.20, p = .06"
    result_all1 = True
    Res, pRes = statcheck([txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9, txt10, txt11, txt12])
    assert all(Res['Decision_Error'].values == result_all1), "Test 1 failed"
########################################################
########################################################
# Test 2 variables
# test if different arguments concerning decision errors work -----------------
# alpha: detect decision errors for different alpha levels

# all cases below are errors

# Test 2
def test_21():
    txt1 = "t(28) = 2.20, p = .06"
    Res, pRes = statcheck(txt1, alpha = .05)
    assert all(Res['Decision_Error'].values == True), "Test 21 failed"

def test_22():
    txt2 = "t(28) = 1.20, p = .03"
    Res, pRes = statcheck(txt2, alpha = .05)
    assert all(Res['Decision_Error'].values == True), "Test 22 failed"

def test_23():
    txt3 = "t(28) = 2.20, p = .11"
    Res, pRes = statcheck(txt3, alpha = .10)
    assert all(Res['Decision_Error'].values == True), "Test 23 failed"

def test_24():
    txt4 = "t(28) = 1.20, p = .09"
    Res, pRes = statcheck(txt4, alpha = .10)
    assert all(Res['Decision_Error'].values == True), "Test 24 failed"

def test_25():
    txt5 = "t(28) = 5.20, p = .02"
    Res, pRes = statcheck(txt5, alpha = .01)
    assert all(Res['Decision_Error'].values == True), "Test 25 failed"

def test_26():
    txt6 = "t(28) = 1.20, p = .005"
    Res, pRes = statcheck(txt6, alpha = .01)
    assert all(Res['Decision_Error'].values == True), "Test 26 failed"


########################################################
########################################################
# Test 3 variables
# pEqualAlphaSig: should p = .05 be considered significant or not


# Test 3
def test_31():
    txt1 = "t(28) = 2.20, p = .05"
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 31 failed"

def test_32():
    txt1 = "t(28) = 2.20, p = .05"
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 32 failed"

# check pEqualAlphaSig for different alpha
def test_33():
    txt2 = "t(28) = 2.20, p = .10"
    Res, pRes = statcheck(txt2, alpha = .10)
    assert all(Res['Decision_Error'].values == False), "Test 33 failed"

def test_34():
    txt2 = "t(28) = 2.20, p = .10"
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False, alpha = .10)
    assert all(Res['Decision_Error'].values == True), "Test 34 failed"

########################################################
########################################################
# Test 4 variables

# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06
t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 4
# if pEqualSig == TRUE
def test_41():
    txt1 = ''.join(["t(28) = ", str(t04), ", p = .04"])
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 41 failed"

def test_42():
    txt2a = ''.join(["t(28) = ", str(t05 + .0001), ", p = .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2a)
    assert all(Res['Decision_Error'].values == False), "Test 42 failed"

def test_43():
    txt3 = ''.join(["t(28) = ", str(t06), ", p = .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == True), "Test 43 failed"

def test_44():
    txt4 = ''.join(["t(28) = ", str(t04), ", p = .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 44 failed"

def test_45():
    txt5 = ''.join(["t(28) = ", str(t05), ", p = .05"])
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == False), "Test 45 failed"

def test_46():
    txt6 = ''.join(["t(28) = ", str(t06), ", p = .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == True), "Test 46 failed"

def test_47():
    txt7 = ''.join(["t(28) = ", str(t04), ", p = .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == True), "Test 47 failed"

def test_48():
    txt8a = ''.join(["t(28) = ", str(t05 + .0001), ", p = .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8a)
    assert all(Res['Decision_Error'].values == True), "Test 48 failed"

def test_49():
    txt9 = ''.join(["t(28) = ", str(t06), ", p = .06"])
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 49 failed"

# if pEqualSig == FALSE
def test_49_1():
    txt1 = ''.join(["t(28) = ", str(t04), ", p = .04"])
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 49_1 failed"

def test_49_2():
    txt2b = ''.join(["t(28) = ", str(t05 - .0001), ", p = .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 49_2 failed"

def test_49_3():
    txt3 = ''.join(["t(28) = ", str(t06), ", p = .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 49_3 failed"

def test_49_4():
    txt4 = ''.join(["t(28) = ", str(t04), ", p = .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 49_4 failed"

def test_49_5():
    txt5 = ''.join(["t(28) = ", str(t05), ", p = .05"])
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 49_5 failed"

def test_49_6():
    txt6 = ''.join(["t(28) = ", str(t06), ", p = .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 49_6 failed"

def test_49_7():
    txt7 = ''.join(["t(28) = ", str(t04), ", p = .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 49_7 failed"

def test_49_8():
    txt8b = ''.join(["t(28) = ", str(t05 - .0001), ", p = .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 49_8 failed"

def test_49_9():
    txt9 = ''.join(["t(28) = ", str(t06), ", p = .06"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 49_9 failed"


########################################################
########################################################
# Test 5 variables
# test statistics exactly reported & p-value < ...

# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06
t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 5

# if pEqualSig == TRUE
def test_51():
    txt1 = ''.join(["t(28) = ", str(t04), ", p < .04"]) # approach computed p == .04
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 51 failed"

def test_52():
    txt2a = ''.join(["t(28) = ", str(t05 + .0001), ", p < .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2a)
    assert all(Res['Decision_Error'].values == False), "Test 52 failed"

def test_53():
    txt3 = ''.join(["t(28) = ", str(t06), ", p < .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == True), "Test 53 failed"

def test_54():
    txt4 = ''.join(["t(28) = ", str(t04), ", p < .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 54 failed"

def test_55():
    txt5a = ''.join(["t(28) = ", str(t05 + .0001), ", p < .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5a)
    assert all(Res['Decision_Error'].values == False), "Test 55 failed"

def test_56():
    txt6 = ''.join(["t(28) = ", str(t06), ", p < .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == True), "Test 56 failed"

def test_57():
    txt7 = ''.join(["t(28) = ", str(t04), ", p < .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == False), "Test 57 failed"

def test_58():
    txt8a = ''.join(["t(28) = ", str(t05 + .0001), ", p < .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8a)
    assert all(Res['Decision_Error'].values == False), "Test 58 failed"

def test_59():
    txt9 = ''.join(["t(28) = ", str(t06), ", p < .06"])
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 59 failed"

# with pEqualSig == FALSE
def test_59_1():
    txt1 = ''.join(["t(28) = ", str(t04), ", p < .04"])
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 59_1 failed"

def test_59_2():
    txt2b = ''.join(["t(28) = ", str(t05 - .0001), ", p < .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 59_2 failed"

def test_59_3():
    txt3 = ''.join(["t(28) = ", str(t06), ", p < .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 59_3 failed"

def test_59_4():
    txt4 = ''.join(["t(28) = ", str(t04), ", p < .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 59_4 failed"

def test_59_5():
    txt5b = ''.join(["t(28) = ", str(t05 - .0001), ", p < .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 59_5 failed"

def test_59_6():
    txt6 = ''.join(["t(28) = ", str(t06), ", p < .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 59_6 failed"

def test_59_7():
    txt7 = ''.join(["t(28) = ", str(t04), ", p < .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 59_7 failed"

def test_59_8():
    txt8b = ''.join(["t(28) = ", str(t05 - .0001), ", p < .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 59_8 failed"

def test_59_9():
    txt9 = ''.join(["t(28) = ", str(t06), ", p < .06"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 59_9 failed"


########################################################
########################################################
# Test 6 variables
# test statistics exactly reported & p-value > ...

# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06
t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 6
# if pEqualSig == TRUE
def test_61():
    txt1 = ''.join(["t(28) = ", str(t04), ", p > .04"]) # approach computed p == .04
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 61 failed"

def test_62():
    txt2a = ''.join(["t(28) = ", str(t05 + .0001), ", p > .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2a)
    assert all(Res['Decision_Error'].values == False), "Test 62 failed"

def test_63():
    txt3 = ''.join(["t(28) = ", str(t06), ", p > .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == False), "Test 63 failed"

def test_64():
    txt4 = ''.join(["t(28) = ", str(t04), ", p > .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == True), "Test 64 failed"

def test_65():
    txt5a = ''.join(["t(28) = ", str(t05 + .0001), ", p > .05"]) # approach computed p == .05
    Res, pRes = statcheck(txt5a)
    assert all(Res['Decision_Error'].values == True), "Test 65 failed"

def test_66():
    txt6 = ''.join(["t(28) = ", str(t06), ", p > .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == False), "Test 66 failed"

def test_67():
    txt7 = ''.join(["t(28) = ", str(t04), ", p > .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == True), "Test 67 failed"

def test_68():
    txt8a = ''.join(["t(28) = ", str(t05 + .0001), ", p > .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8a)
    assert all(Res['Decision_Error'].values == True), "Test 68 failed"

def test_69():
    txt9 = ''.join(["t(28) = ", str(t06), ", p > .06"])
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 69 failed"

# with pEqualSig == FALSE

def test_69_1():
    txt1 = ''.join(["t(28) = ", str(t04), ", p > .04"])
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_1 failed"

def test_69_2():
    txt2b = ''.join(["t(28) = ", str(t05 - .0001), ", p > .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_2 failed"

def test_69_3():
    txt3 = ''.join(["t(28) = ", str(t06), ", p > .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_3 failed"

def test_69_4():
    txt4 = ''.join(["t(28) = ", str(t04), ", p > .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 69_4 failed"

def test_69_5():
    txt5b = ''.join(["t(28) = ", str(t05 - .0001), ", p > .05"]) # approach computed p == .05
    Res, pRes = statcheck(txt5b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_5 failed"

def test_69_6():
    txt6 = ''.join(["t(28) = ", str(t06), ", p > .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_6 failed"

def test_69_7():
    txt7 = ''.join(["t(28) = ", str(t04), ", p > .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 69_7 failed"

def test_69_8():
    txt8b = ''.join(["t(28) = ", str(t05 - .0001), ", p > .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8b, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_8 failed"

def test_69_9():
    txt9 = ''.join(["t(28) = ", str(t06), ", p > .06"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 69_9 failed"

########################################################
########################################################
# Test 7 variables
# test statistics < & p-value exactly reported
# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06

t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 7
# if pEqualSig == TRUE
def test_71():
    txt1 = ''.join(["t(28) < ", str(t04 - 0.001), ", p = .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 71 failed"

def test_72():
    txt2 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p = .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2)
    assert all(Res['Decision_Error'].values == True), "Test 72 failed"

def test_73():
    txt3 = ''.join(["t(28) < ", str(t06), ", p = .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == True), "Test 73 failed"

def test_74():
    txt4 = ''.join(["t(28) < ", str(t04), ", p = .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 74 failed"

def test_75():
    txt5 = ''.join(["t(28) < ", str(t05 - 0.001), ", p = .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == True), "Test 75 failed"

def test_76():
    txt6 = ''.join(["t(28) < ", str(t06), ", p = .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == True), "Test 76 failed"

def test_77():
    txt7 = ''.join(["t(28) < ", str(t04), ", p = .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == False), "Test 77 failed"

def test_78():
    txt8 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p = .0600"]) # approach computed p == .05
    Res, pRes = statcheck(txt8)
    assert all(Res['Decision_Error'].values == False), "Test 78 failed"

def test_79():
    txt9 = ''.join(["t(28) < ", str(t06), ", p = .0600"]) # approach computed p == .06
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 79 failed"

# with pEqualSig == FALSE

def test_79_1():
    txt1 = ''.join(["t(28) < ", str(t04 - 0.001), ", p = .0400"])
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_1 failed"

def test_79_2():
    txt2 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p = .04"])
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 79_2 failed"

def test_79_3():
    txt3 = ''.join(["t(28) < ", str(t06), ", p = .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 79_3 failed"

def test_79_4():
    txt4 = ''.join(["t(28) < ", str(t04), ", p = .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_4 failed"

def test_79_5():
    txt5 = ''.join(["t(28) < ", str(t05 - 0.001), ", p = .0500"])
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_5 failed"

def test_79_6():
    txt6 = ''.join(["t(28) < ", str(t06), ", p = .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_6 failed"

def test_79_7():
    txt7 = ''.join(["t(28) < ", str(t04), ", p = .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_7 failed"

def test_79_8():
    txt8 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p = .0600"])
    Res, pRes = statcheck(txt8, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_8 failed"

def test_79_9():
    txt9 = ''.join(["t(28) < ", str(t06), ", p = .0600"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 79_9 failed"

########################################################
########################################################
# Test 8 variables
# test statistics < & p-value <

# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06

t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 8
# if pEqualSig == TRUE
def test_81():
    txt1 = ''.join(["t(28) < ", str(t04), ", p < .04"])
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 81 failed"

def test_82():
    txt2 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p < .04"])  # approach computed p == .05
    Res, pRes = statcheck(txt2)
    assert all(Res['Decision_Error'].values == True), "Test 82 failed"

def test_83():
    txt3 = ''.join(["t(28) < ", str(t06), ", p < .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == True), "Test 83 failed"

def test_84():
    txt4 = ''.join(["t(28) < ", str(t04), ", p < .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 84 failed"

def test_85():
    txt5 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p < .05"]) # approach computed p == .05
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == True), "Test 85 failed"

def test_86():
    txt6 = ''.join(["t(28) < ", str(t06), ", p < .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == True), "Test 86 failed"

def test_87():
    txt7 = ''.join(["t(28) < ", str(t04), ", p < .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == False), "Test 87 failed"

def test_88():
    txt8 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p < .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8)
    assert all(Res['Decision_Error'].values == False), "Test 88 failed"

def test_89():
    txt9 = ''.join(["t(28) < ", str(t06), ", p < .06"])
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 89 failed"

# with pEqualSig == FALSE

def test_89_1():
    txt1 = ''.join(["t(28) < ", str(t04), ", p < .04"])
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 89_1 failed"

def test_89_2():
    txt2 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p < .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 89_2 failed"

def test_89_3():
    txt3 = ''.join(["t(28) < ", str(t06), ", p < .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 89_3 failed"

def test_89_4():
    txt4 = ''.join(["t(28) < ", str(t04), ", p < .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 89_4 failed"

def test_89_5():
    txt5 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p < .05"]) # approach computed p == .05
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 89_5 failed"

def test_89_6():
    txt6 = ''.join(["t(28) < ", str(t06), ", p < .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 89_6 failed"

def test_89_7():
    txt7 = ''.join(["t(28) < ", str(t04), ", p < .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 89_7 failed"

def test_89_8():
    txt8 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p < .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 89_8 failed"

def test_89_9():
    txt9 = ''.join(["t(28) < ", str(t06), ", p < .06"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 89_9 failed"

########################################################
########################################################
# Test 9 variables
# test statistics < & p-value >
# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06

t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 9
# if pEqualSig == TRUE
def test_91():
    txt1 = ''.join(["t(28) < ", str(t04), ", p > .04"])
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 91 failed"

def test_92():
    txt2 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p > .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2)
    assert all(Res['Decision_Error'].values == False), "Test 92 failed"

def test_93():
    txt3 = ''.join(["t(28) < ", str(t06), ", p > .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == False), "Test 93 failed"

def test_94():
    txt4 = ''.join(["t(28) < ", str(t04), ", p > .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 94 failed"

def test_95():
    txt5 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p > .05"]) # approach computed p == .05
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == False), "Test 95 failed"

def test_96():
    txt6 = ''.join(["t(28) < ", str(t06), ", p > .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == False), "Test 96 failed"

def test_97():
    txt7 = ''.join(["t(28) < ", str(t04), ", p > .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == False), "Test 97 failed"

def test_98():
    txt8 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p > .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8)
    assert all(Res['Decision_Error'].values == False), "Test 98 failed"

def test_99():
    txt9 = ''.join(["t(28) < ", str(t06), ", p > .06"])
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 99 failed"

# with pEqualSig == FALSE

def test_99_1():
    txt1 = ''.join(["t(28) < ", str(t04), ", p > .04"])
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_1 failed"

def test_99_2():
    txt2 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p > .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_2 failed"

def test_99_3():
    txt3 = ''.join(["t(28) < ", str(t06), ", p > .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_3 failed"

def test_99_4():
    txt4 = ''.join(["t(28) < ", str(t04), ", p > .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_4 failed"

def test_99_5():
    txt5 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p > .05"]) # approach computed p == .05
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_5 failed"

def test_99_6():
    txt6 = ''.join(["t(28) < ", str(t06), ", p > .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_6 failed"

def test_99_7():
    txt7 = ''.join(["t(28) < ", str(t04), ", p > .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_7 failed"

def test_99_8():
    txt8 = ''.join(["t(28) < ", str(t05 - 0.0001), ", p > .06"]) # approach computed p == .05
    Res, pRes = statcheck(txt8, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_8 failed"

def test_99_9():
    txt9 = ''.join(["t(28) < ", str(t06), ", p > .06"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 99_9 failed"

########################################################
########################################################
# Test 10 variables
# test statistics > & p-value exactly reported
# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06

t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 10
# if pEqualSig == TRUE
def test_101():
    txt1 = ''.join(["t(28) > ", str(t04 + 0.001), ", p = .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 101 failed"

def test_102():
    txt2 = ''.join(["t(28) > ", str(t05 + 0.001), ", p = .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2)
    assert all(Res['Decision_Error'].values == False), "Test 102 failed"

def test_103():
    txt3 = ''.join(["t(28) > ", str(t06), ", p = .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == False), "Test 103 failed"

def test_104():
    txt4 = ''.join(["t(28) > ", str(t04), ", p = .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 104 failed"

def test_105():
    txt5 = ''.join(["t(28) > ", str(t05 + 0.001), ", p = .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == False), "Test 105 failed"

def test_106():
    txt6 = ''.join(["t(28) > ", str(t06), ", p = .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == False), "Test 106 failed"

def test_107():
    txt7 = ''.join(["t(28) > ", str(t04), ", p = .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == True), "Test 107 failed"

def test_108():
    txt8 = ''.join(["t(28) > ", str(t05 + 0.001), ", p = .0600"]) # approach computed p == .05
    Res, pRes = statcheck(txt8)
    assert all(Res['Decision_Error'].values == True), "Test 108 failed"

def test_109():
    txt9 = ''.join(["t(28) > ", str(t06 + 0.001), ", p = .0600"]) # approach computed p == .06
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 109 failed"

# with pEqualSig == FALSE

def test_109_1():
    txt1 = ''.join(["t(28) > ", str(t04 + 0.001), ", p = .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 109_1 failed"

def test_109_2():
    txt2 = ''.join(["t(28) > ", str(t05 + 0.001), ", p = .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 109_2 failed"

def test_109_3():
    txt3 = ''.join(["t(28) > ", str(t06), ", p = .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 109_3 failed"

def test_109_4():
    txt4 = ''.join(["t(28) > ", str(t04), ", p = .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 109_4 failed"

def test_109_5():
    txt5 = ''.join(["t(28) > ", str(t05 + 0.001), ", p = .0500"])
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 109_5 failed"

def test_109_6():
    txt6 = ''.join(["t(28) > ", str(t06), ", p = .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 109_6 failed"

def test_109_7():
    txt7 = ''.join(["t(28) > ", str(t04), ", p = .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 109_7 failed"

def test_109_8():
    txt8 = ''.join(["t(28) > ", str(t05 + 0.001), ", p = .0600"])
    Res, pRes = statcheck(txt8, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 109_8 failed"

def test_109_9():
    txt9 = ''.join(["t(28) > ", str(t06 + 0.001), ", p = .0600"])
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 109_9 failed"

########################################################
########################################################
# Test 11 variables
# test statistics > & p-value <
# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06

t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 11
# if pEqualSig == TRUE
def test_111():
    txt1 = ''.join(["t(28) > ", str(t04 + 0.001), ", p < .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 111 failed"

def test_112():
    txt2 = ''.join(["t(28) > ", str(t05 + 0.001), ", p < .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2)
    assert all(Res['Decision_Error'].values == False), "Test 112 failed"

def test_113():
    txt3 = ''.join(["t(28) > ", str(t06), ", p < .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == False), "Test 113 failed"

def test_114():
    txt4 = ''.join(["t(28) > ", str(t04), ", p < .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == False), "Test 114 failed"

def test_115():
    txt5 = ''.join(["t(28) > ", str(t05 + 0.001), ", p < .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == False), "Test 115 failed"

def test_116():
    txt6 = ''.join(["t(28) > ", str(t06), ", p < .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == False), "Test 116 failed"

def test_117():
    txt7 = ''.join(["t(28) > ", str(t04), ", p < .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == False), "Test 117 failed"

def test_118():
    txt8 = ''.join(["t(28) > ", str(t05 + 0.001), ", p < .0600"])  # approach computed p == .05
    Res, pRes = statcheck(txt8)
    assert all(Res['Decision_Error'].values == False), "Test 118 failed"

def test_119():
    txt9 = ''.join(["t(28) > ", str(t06 + 0.001), ", p < .0600"]) # approach computed p == .06
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 119 failed"

# with pEqualSig == FALSE

def test_119_1():
    txt1 = ''.join(["t(28) > ", str(t04 + 0.001), ", p < .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_1 failed"

def test_119_2():
    txt2 = ''.join(["t(28) > ", str(t05 + 0.001), ", p < .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_2 failed"

def test_119_3():
    txt3 = ''.join(["t(28) > ", str(t06), ", p < .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_3 failed"

def test_119_4():
    txt4 = ''.join(["t(28) > ", str(t04), ", p < .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_4 failed"

def test_119_5():
    txt5 = ''.join(["t(28) > ", str(t05 + 0.001), ", p < .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_5 failed"

def test_119_6():
    txt6 = ''.join(["t(28) > ", str(t06), ", p < .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_6 failed"

def test_119_7():
    txt7 = ''.join(["t(28) > ", str(t04), ", p < .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_7 failed"

def test_119_8():
    txt8 = ''.join(["t(28) > ", str(t05 + 0.001), ", p < .0600"]) # approach computed p == .05
    Res, pRes = statcheck(txt8, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_8 failed"

def test_119_9():
    txt9 = ''.join(["t(28) > ", str(t06 + 0.001), ", p < .0600"]) # approach computed p == .06
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 119_9 failed"

########################################################
########################################################
# Test 12 variables
# test statistics > & p-value >
# assume alpha = .05
# calculate which t-values correspond to p-values of .04, .05, and .06

t04 = - t.ppf(.04 / 2, 28)
t05 = - t.ppf(.05 / 2, 28)
t06 = - t.ppf(.06 / 2, 28)

# Test 12
# if pEqualSig == TRUE
def test_121():
    txt1 = ''.join(["t(28) > ", str(t04 + 0.001), ", p > .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1)
    assert all(Res['Decision_Error'].values == False), "Test 121 failed" # approach computed p == .05

def test_122():
    txt2 = ''.join(["t(28) > ", str(t05 + 0.0001), ", p > .04"])
    Res, pRes = statcheck(txt2)
    assert all(Res['Decision_Error'].values == False), "Test 122 failed"

def test_123():
    txt3 = ''.join(["t(28) > ", str(t06), ", p > .04"])
    Res, pRes = statcheck(txt3)
    assert all(Res['Decision_Error'].values == False), "Test 123 failed"

def test_124():
    txt4 = ''.join(["t(28) > ", str(t04), ", p > .05"])
    Res, pRes = statcheck(txt4)
    assert all(Res['Decision_Error'].values == True), "Test 124 failed"

def test_125():
    txt5 = ''.join(["t(28) > ", str(t05 + 0.001), ", p > .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5)
    assert all(Res['Decision_Error'].values == True), "Test 125 failed"

def test_126():
    txt6 = ''.join(["t(28) > ", str(t06), ", p > .05"])
    Res, pRes = statcheck(txt6)
    assert all(Res['Decision_Error'].values == False), "Test 126 failed"

def test_127():
    txt7 = ''.join(["t(28) > ", str(t04), ", p > .06"])
    Res, pRes = statcheck(txt7)
    assert all(Res['Decision_Error'].values == True), "Test 127 failed"

def test_128():
    txt8 = ''.join(["t(28) > ", str(t05 + 0.001), ", p > .0600"]) # approach computed p == .05
    Res, pRes = statcheck(txt8)
    assert all(Res['Decision_Error'].values == True), "Test 128 failed"

def test_129():
    txt9 = ''.join(["t(28) > ", str(t06 + 0.001), ", p > .0600"]) # approach computed p == .06
    Res, pRes = statcheck(txt9)
    assert all(Res['Decision_Error'].values == False), "Test 129 failed"

# with pEqualSig == FALSE

def test_129_1():
    txt1 = ''.join(["t(28) > ", str(t04 + 0.001), ", p > .0400"]) # approach computed p == .04
    Res, pRes = statcheck(txt1, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 129_1 failed"

def test_129_2():
    txt2 = ''.join(["t(28) > ", str(t05 + 0.0001), ", p > .04"]) # approach computed p == .05
    Res, pRes = statcheck(txt2, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 129_2 failed"

def test_129_3():
    txt3 = ''.join(["t(28) > ", str(t06), ", p > .04"])
    Res, pRes = statcheck(txt3, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 129_3 failed"

def test_129_4():
    txt4 = ''.join(["t(28) > ", str(t04), ", p > .05"])
    Res, pRes = statcheck(txt4, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 129_4 failed"

def test_129_5():
    txt5 = ''.join(["t(28) > ", str(t05 + 0.001), ", p > .0500"]) # approach computed p == .05
    Res, pRes = statcheck(txt5, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 129_5 failed"

def test_129_6():
    txt6 = ''.join(["t(28) > ", str(t06), ", p > .05"])
    Res, pRes = statcheck(txt6, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 129_6 failed"

def test_129_7():
    txt7 = ''.join(["t(28) > ", str(t04), ", p > .06"])
    Res, pRes = statcheck(txt7, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 129_7 failed"

def test_129_8():
    txt8 = ''.join(["t(28) > ", str(t05 + 0.001), ", p > .0600"]) # approach computed p == .05
    Res, pRes = statcheck(txt8, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == True), "Test 129_8 failed"

def test_129_9():
    txt9 = ''.join(["t(28) > ", str(t06 + 0.001), ", p > .0600"]) # approach computed p == .06
    Res, pRes = statcheck(txt9, pEqualAlphaSig = False)
    assert all(Res['Decision_Error'].values == False), "Test 129_9 failed"