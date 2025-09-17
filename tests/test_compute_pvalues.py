import sys
import os
import scipy.stats as stats
import numpy as np
from statcheck.compute_p import r2t
from statcheck.st import statcheck

# python tests for the p-value correction

# Test variables

txt1 = "t(28) = 2.20, p = .03"
computed1 = stats.t.cdf(-1 * abs(2.20), 28) * 2

txt2 = "F(2, 28) = 2.20, p = .15"
computed2 = stats.f.sf(2.20, 2, 28)

txt3 = "r(28) = .22, p = .26"
computed3 = np.minimum(stats.t.cdf(-1 * abs(r2t(.22, 28)), 28) * 2, 1)

txt4 = " z = 2.20, p = .04"
computed4 = stats.norm.sf(abs(2.20)) * 2

txt5 = "chi2(28) = 22.20, p = .79"
computed5 = stats.chi2.sf(22.20, 28)

txt6 = "Q(28) = 22.20, p = .79"
computed6 = stats.chi2.sf(22.20, 28)

# test 1
def test_pvalue1():
    Res, pRes = statcheck(txt1)
    assert Res['Computed_P_Value'].iloc[0] == computed1, "Test 1 failed"

# test 2
def test_pvalue2():
    Res, pRes = statcheck(txt2)
    assert Res['Computed_P_Value'].iloc[0] == computed2, "Test 2 failed"

# test 3
def test_pvalue3():
    Res, pRes = statcheck(txt3)
    assert Res['Computed_P_Value'].iloc[0] == computed3, "Test 3 failed"

# test 4
def test_pvalue4():
    Res, pRes = statcheck(txt4)
    assert Res['Computed_P_Value'].iloc[0] == computed4, "Test 4 failed"

# test 5
def test_pvalue5():
    Res, pRes = statcheck(txt5)
    assert Res['Computed_P_Value'].iloc[0] == computed5, "Test 5 failed"

# test 6
def test_pvalue6():
    Res, pRes = statcheck(txt6)
    assert Res['Computed_P_Value'].iloc[0] == computed6, "Test 6 failed"




