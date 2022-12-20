import numpy as np
import scipy.stats as stats
from math import sqrt


def compute_p(test_type, test_stat, df1, df2, two_tailed):
    """
    Compute p-value for a given test statistic and degrees of freedom
    :param test_type: Type of test (e.g. t-test, F-test, chi-square test)
    :param test_stat: Test statistic
    :param df1: Degrees of freedom 1
    :param df2: Degrees of freedom 2
    :param two_tailed: Whether the test is two-tailed
    :return: p-value
    """
    if test_type not in ["t", "F", "Z", "r", "Chi2", "Q", "Qb", "Qw"]:
        raise ValueError("test_type must be one of t, F, Z, r, Chi2, Q, Qb, Qw")


    # compute p-values ---------------------------------------------------------

    if test_type == "t":
        computed = stats.t.cdf(-1 * abs(test_stat), df2)

    elif test_type == "F":
        computed = stats.f.sf(test_stat, df1, df2)

    elif test_type == "Z":
        computed = stats.norm.sf(abs(test_stat))

    elif test_type == "r":
        t = r2t(test_stat, df2)
        computed = stats.t.cdf(-1 * abs(t), df2)

    elif test_type == "Chi2" or test_type == "Q" or test_type == "Qb" or test_type == "Qw":
        computed = stats.chi2.sf(test_stat, df1)

    # compute two-tailed ------------------------------------------------------

    if (not np.isnan(computed)) and (test_type == "t" or test_type == "Z" or test_type == "r") and two_tailed:
        computed = computed * 2

    # return ------------------------------------------------------------------

    return computed

def r2t(r, df):
    """
    Convert correlation coefficient to t-statistic
    :param r: Correlation coefficient
    :param df: Degrees of freedom
    :return: t-statistic
    """
    t = r / (sqrt((1 - r**2) / df))
    return t