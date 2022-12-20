from st.regex import *
import pandas as pd
pd.options.mode.chained_assignment = None
import re
import numpy as np

# this script contains helper functions to extract and parse nhst results from
# text

# function to extract snippets of text from a string ---------------------------

def extract_pattern(txt, pattern, ignore_case=True, return_limits = False):
    # extract the locations of the matches in the text:
    # gregexpr returns the position of every match in a string
    # if there are multiple matches in the text, gregexpr will flag them all
    # the output is in list format, but the relevant information is all in [[1]]
    txt = txt.replace('\n', ' ')

    string_loc = re.finditer(pattern, txt, re.IGNORECASE)

    # if no match is found, return NULL
    if string_loc is None:
        return None

    # if a match is found:
    # extract the raw text of the regex match:
    # retrieve a 'substring' from the text that starts at string_loc: string_loc
    # is a vector of integers that indicate the location of the first characters of
    # the match. The end point of the substring is determined using the
    # attribute 'match.length' of string_loc This is a vector of integers indicating
    # how long each matched string is. By adding the length of the string to the
    # position of the first character, and subtracting 1, you obtain the location
    # of the last character of the string.
    string_list = []
    starts_list = []
    ends_list = []
    for m in string_loc:
        start_index = m.start()
        end_index = m.end()
        string_list.append(txt[start_index:end_index])
        starts_list.append(start_index)
        ends_list.append(end_index)

    if return_limits == True:
        return string_list, starts_list, ends_list
    else:
        return string_list



# function to extract dfs from a raw nhst result -------------------------------

def extract_df(raw, test_type):
    # z tests do not have dfs, so return df1 = NA, and df2 = NA for z-tests
    if test_type == "Z":
        df1 = None
        df2 = None
    else:
        # for all other test types, extract dfs from the raw nhst result
        df_raw = extract_pattern(txt=raw, pattern=RGX_DF)[0]

        # remove parentheses to only keep numbers
        df = re.sub(r"\(|\)", "", df_raw)

        # split string on comma to separate df1 and df2 / N
        # note: there can be no commas as thousand separators in the dfs; statcheck
        # would not have recognized these in the first place, so we don't have to take
        # this possibility into account here
        df = re.split(r",", df)

        # remove leading/trailing whitespaces
        df = [x.strip() for x in df]

        # there are three different types of degrees of freedom:
        # - t-tests, correlations, and Q-tests (a single number between brackets)
        # - F-tests (two degrees of freedom separated by a comma)
        # - chi2 (can also contain sample size)


        if test_type in ["t", "r"]:
            df1 = None
            df2 = df[0]

        elif test_type == "F":

            # for some reason, typesetting in articles sometimes goes wrong with
            # F-tests and when df1 == 1, it gets typeset as the letter l or I
            # If this happens, replace the l or I with a 1

            if re.search(RGX_DF1_I_L, df[0]):
                df[0] = 1

            df1 = df[0]
            df2 = df[1]

        elif test_type in ["Chi2", "Q", "Qw", "Qb"]:
            df1 = df[0]
            df2 = None
        else:
            df1 = None
            df2 = None
    # return dataframe with scalar values
    return pd.DataFrame({"df1": df1,
                            "df2": df2},
                            index=[0])


def remove_1000_sep(raw):
    # replace all matches in the raw nhst results with nothing
    output = re.sub(pattern=RGX_1000_SEP,
                    repl="",
                    string=raw,
                    flags=re.DOTALL | re.VERBOSE) # for the lookaheads & lookbehinds in the regex
    return output


# function to replace weird symbols with a minus sign --------------------------

# sometimes the mathematical symbol for a minus sign is wrongly converted into
# a strange symbol. Since it is very likely that any weird symbol in front of
# a test statistic is in fact a minus sign, replace all such weird codings with
# an actual minus sign


def recover_minus_sign(raw):
    output = re.sub(pattern=RGX_WEIRD_MINUS,
             repl=" -",
             string=raw,
             flags=re.VERBOSE)

    return output

# function to extract test-values and test comparisons -------------------------

def extract_test_stats(raw):
    # remove N = ... from chi-square tests
    # otherwise, these sample sizes will wrongly be classified as test statistics
    raw_noN = re.sub(RGX_DF_CHI2, "", raw)

    # extract test comparison and test value
    test_raw = extract_pattern(txt=raw_noN, pattern=RGX_TEST_VALUE)[0]

    # extract test comparison
    test_comp = extract_pattern(txt=test_raw, pattern=RGX_COMP)

    # remove test comparison to only keep numbers
    test_value = re.sub(RGX_COMP, "", test_raw)
    test_value = test_value.replace('− ', ' -')

    # remove thousand separators
    test_value = remove_1000_sep(test_value)

    # replace weird coding before a test value with a minus sign
    test_value = recover_minus_sign(test_value)

    # remove leading/trailing whitespaces
    test_value = test_value.strip()

    # remove comma at the end of the value
    test_value = re.sub(",$", "", test_value)


    # record the number of decimals of the test statistic
    if '.' in test_value or ',' in test_value:
        test_dec = len(test_value.split(".")[1])
    else:
        test_dec = 0
    if test_dec < 0:
        test_dec = 0

    # # if there is a space right before the decimal point, and there are no numbers behind it,
    # # subsitute the space with a zero
    # test_value = re.sub(" \.", " 0.", test_value)
    # # remove spaces
    # test_value = re.sub(" ", "", test_value)

    # make test_value numeric; suppress warnings (these could arive if the test
    # value is unusual, e.g., a weird minus followed by a space can't be made
    # numeric)
    # note: this needs to happen AFTER extracting the nr of decimals
    test_value = float(test_value)
    # return dataframe with scalar values
    return pd.DataFrame({"test_comp": test_comp,
                         'test_value': test_value,
                         'test_dec': test_dec},
                        index=[0])



# function to extract and parse p-values --------------------------------------

def extract_p_value(raw):
    p_raw = extract_pattern(txt=raw,
                            pattern=RGX_P_NS)

    p_comp = []
    p_value = []
    p_dec = []

    for i in range(len(p_raw)):
        if bool(re.search(pattern=RGX_NS, string=p_raw[i], flags=re.IGNORECASE)):
            p_comp.append('ns')
            p_value.append(np.nan)
            p_dec.append(np.nan)
        else:
            # extract p-comparison
            p_comp.append(extract_pattern(txt=p_raw[i],
                                          pattern=RGX_COMP))

            # remove p comparison to only keep numbers
            # split the string on the comparison, that splits the string into a p and
            # the actual value. Only select the second element: the value
            p_value.append(re.split(pattern=RGX_COMP, string=p_raw[i])[1])

            # remove leading/trailing whitespaces

            # record the number of decimals of the p-value
            dec = re.search(pattern=RGX_DEC, string=p_value[i]).end() - 2 # not sure
            if dec < 0:
                dec = 0

            p_value[i] = float(p_value[i])

            p_dec.append(dec)

        p_comp = [x[0] if isinstance(x, list) else x for x in p_comp]

    return pd.DataFrame({"p_comp": p_comp,
                         "p_value": p_value,
                         "p_dec": p_dec})