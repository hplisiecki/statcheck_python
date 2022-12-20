from statcheck.compute_p import compute_p



def error_test(reported_p, test_type, test_stat,
               df1, df2,
               p_comparison, test_comparison,
               p_dec, test_dec,
               two_tailed,
               alpha, pZeroError):
    """
    Check if a result is an error
    :param reported_p: Reported p-value
    :param test_type: Type of test (e.g. t-test, F-test, chi-square test)
    :param test_stat: Test statistic
    :param df1: Degrees of freedom 1
    :param df2: Degrees of freedom 2
    :param p_comparison: Comparison of reported p-value to computed p-value
    :param test_comparison: Comparison of reported test statistic to computed test statistic
    :param p_dec: Number of decimal places to round p-values to
    :param test_dec: Number of decimal places to round test statistics to
    :param two_tailed: Whether the test is two-tailed
    :param alpha: Significance level
    :param pZeroError: Whether to treat p-values of 0 as errors
    :return:
    """
    try:
        reported_p = float(reported_p)
    except:
        pass

    # replace 'ns' for > alpha -----------------------------------------------
    if p_comparison == 'ns':
        reported_p = alpha
    else:
        p_dec = int(p_dec)
    if p_comparison == 'ns':
        p_comparison = ">"

    # compute p-values -------------------------------------------------------

    # take into account that the reported test statistic may have been rounded
    # to that end, compute the upper and lower bound of the test statistic
    # based on the number of decimals that it was reported with. E.g.,
    # a t-value of 2.0 could have been rounded from anywhere between 1.95-2.05.
    low_stat = test_stat - (.5 / 10 ** test_dec)
    up_stat = test_stat + (.5 / 10 ** test_dec)

    # Compute the p-values that belong to the upper and lower bound of the test
    # statistic. This is the range of p-values that would be correct.
    up_p = compute_p(test_type=test_type,
                     test_stat=low_stat,
                     df1=df1,
                     df2=df2,
                     two_tailed=two_tailed)

    low_p = compute_p(test_type=test_type,
                      test_stat=up_stat,
                      df1=df1,
                      df2=df2,
                      two_tailed=two_tailed)

    # p values smaller or equal to zero are errors ---------------------------

    # import pdb; pdb.set_trace()

    if (pZeroError == True) and (reported_p <= 0):
        error = True
        return (error)

        # check errors for different combinations of <>= -------------------------

    if test_comparison == "=":

        if p_comparison == "=":

            error = (reported_p > round(up_p, p_dec)) | (reported_p < round(low_p, p_dec))
            return error

        elif p_comparison == "<":

            error = reported_p < low_p
            return error

        elif p_comparison == ">":

            error = reported_p > up_p
            return error


    elif test_comparison == "<":

        if p_comparison == "=":
            error = reported_p < round(up_p, p_dec)
            return error

        elif p_comparison == "<":
            error = reported_p < up_p
            return error

        elif p_comparison == ">":
            error = False
            return error


    elif test_comparison == ">":

        if p_comparison == "=":
            error = reported_p > round(low_p, p_dec)
            return error

        elif p_comparison == "<":
            error = False
            return error

        elif p_comparison == ">":
            error = reported_p > low_p
            return error

    return None

