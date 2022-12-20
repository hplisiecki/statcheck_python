def decision_error_test(reported_p, computed_p, test_comparison, p_comparison, alpha, pEqualAlphaSig):
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