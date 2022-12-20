def decision_error_test(reported_p, computed_p, test_comparison, p_comparison, alpha, pEqualAlphaSig):
    """
    Check if a result is a decision error.
    :param reported_p: reported p-value
    :param computed_p: computed p-value
    :param test_comparison: test comparison
    :param p_comparison: p-value comparison
    :param alpha: significance level
    :param pEqualAlphaSig: if True, p-values equal to alpha are considered significant
    :return: True if the result is a decision error, False otherwise
    """
    if reported_p == 'ns':
        reported_p = alpha

    if p_comparison == 'ns':
        p_comparison = ">"

    # import pdb; pdb.set_trace()

    if pEqualAlphaSig == True:
        if test_comparison == "=":
            if p_comparison == "=":
                dec_error = ((reported_p <= alpha) & (computed_p > alpha)) or ((reported_p > alpha) & (computed_p <= alpha))
                return dec_error
            elif p_comparison == "<":
                dec_error = (reported_p <= alpha) & (computed_p > alpha)
                return dec_error
            elif p_comparison == ">":
                dec_error = (reported_p >= alpha) & (computed_p <= alpha)
                return dec_error
        elif test_comparison == "<":
            if p_comparison == "=":
                dec_error = (reported_p <= alpha) & (computed_p >= alpha)
                return dec_error
            elif p_comparison == "<":
                dec_error = (reported_p <= alpha) & (computed_p >= alpha)
                return dec_error
            elif p_comparison == ">":
                dec_error = False
                return dec_error
        elif test_comparison == ">":
            if p_comparison == "=":
                dec_error = (reported_p > alpha) & (computed_p <= alpha)
                return dec_error
            elif p_comparison == "<":
                dec_error = False
                return dec_error
            elif p_comparison == ">":
                dec_error = (reported_p >= alpha) & (computed_p <= alpha)
                return dec_error
        return None
    elif pEqualAlphaSig == False:
        if test_comparison == "=":
            if p_comparison == "=":
                dec_error = ((reported_p < alpha) & (computed_p >= alpha)) or ((reported_p >= alpha) & (computed_p < alpha))
                return dec_error
            elif p_comparison == "<":
                dec_error = (reported_p <= alpha) & (computed_p >= alpha)
                return dec_error
            elif p_comparison == ">":
                dec_error = (reported_p >= alpha) & (computed_p < alpha)
                return dec_error
        elif test_comparison == "<":
            if p_comparison == "=":
                dec_error = (reported_p < alpha) & (computed_p >= alpha)
                return dec_error
            elif p_comparison == "<":
                dec_error = (reported_p <= alpha) & (computed_p >= alpha)
                return dec_error
            elif p_comparison == ">":
                dec_error = False
                return dec_error
        elif test_comparison == ">":
            if p_comparison == "=":
                dec_error = (reported_p >= alpha) & (computed_p <= alpha)
                return dec_error
            elif p_comparison == "<":
                dec_error = False
                return dec_error
            elif p_comparison == ">":
                dec_error = (reported_p >= alpha) & (computed_p <= alpha)
                return dec_error
        return None