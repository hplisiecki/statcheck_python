from statcheck.helpers_parse_stats import extract_pattern
from statcheck.regex import *
from statcheck.helpers_parse_stats import extract_df
from statcheck.helpers_parse_stats import extract_test_stats
from statcheck.helpers_parse_stats import extract_p_value

import pandas as pd
pd.options.mode.chained_assignment = None
import re

def extract_stats(txt, stat, name):
    """
    Extracts the test statistic, degrees of freedom, and p-value from a string.
    :param txt: String with the text to be parsed
    :param stat: Types of statistical test
    :param name: Names of source files
    :return:
    """
    # step 1: extract the raw nhst results ------------------------------------------
    # extract the raw results from the text
    nhst_raw, starts_list, ends_list = extract_pattern(txt, # nhst is the regex for nhst results
                               RGX_NHST,
                               ignore_case=False,
                                          return_limits=True)
    # if e present at the end of one of the strings
    nhst_new = []
    for idx, nhst in enumerate(nhst_raw):
        if nhst.endswith('e') or nhst.endswith('E'):
            # find where the specific nhst ends in the text
            end = ends_list[idx]

            # find the first couple of numbers after the nhst
            RGX_NUMBERS = re.compile(r'\d+')
            numbers = re.findall(RGX_NUMBERS, txt[end:end+10])[0]
            # if there are numbers, add them to the nhst
            if len(numbers) > 0:
                nhst = nhst + '-' + numbers
            # remove the nhst from the list
        # if the first character is '='
        if nhst.strip().startswith('='):
            start = starts_list[idx]
            # find the first couple of characters before the nhst (this includes the χ character)
            letters = txt[start-10:start].split(' ')[-1]
            # if there are letters, add them to the nhst
            if len(letters) > 0:
                nhst = letters + nhst

        nhst_new.append(nhst)
    nhst_raw = nhst_new

    # if there are no nhst results in the text, return an empty data frame
    if len(nhst_raw) == 0:
        return pd.DataFrame()

    # step 2: parse the extracted results ------------------------------------------

    # empty vectors and data frames to store results in
    # where relevant, force the output to be of type "character"
    test_type = []
    df_result = pd.DataFrame()
    test_stats = pd.DataFrame()
    pvals = pd.DataFrame()

    # loop over all extracted, raw nhst results
    # each nhst result is parsed individually, in the order that they were extracted
    # from the text
    for i in range(len(nhst_raw)):

        # extract the test types from the nhst results
        test_raw = extract_pattern(nhst_raw[i], RGX_TEST_TYPE)[0]

        # classify the test types in standard classifications

        # for each test type, check where the vector with extracted, raw test types
        # matches the regex for each test type, and assign the appropriate category
        # the order of the classification matters: Q has to be tested first,
        # otherwise the regex for t will also match Qwithin and Qbetween, because
        # both have a t in them. Similarly: first check for Qb, because Qbetween
        # also has a w in it
        if re.search(RGX_Q, test_raw):
            # distinguish between Q, Qw, and Qb
            if re.search(RGX_QB, test_raw):
                test_type.append("Qb")
            elif re.search(RGX_QW, test_raw):
                test_type.append("Qw")
            else:
                test_type.append("Q")
        elif re.search(RGX_T, test_raw):
            test_type.append("t")
        elif re.search(RGX_F, test_raw):
            test_type.append("F")
        elif re.search(RGX_R, test_raw):
            test_type.append("r")
        elif re.search(RGX_Z, test_raw):
            test_type.append("Z")
        elif re.search(RGX_CHI2, test_raw):
            test_type.append("Chi2")
        else:
            test_type.append("None")
            dfs = pd.DataFrame({"df1": None,
                                "df2": None},
                                index=[0])
            df_result = pd.concat([df_result, dfs], axis=0)
            test = pd.DataFrame({"test_comp": None,
                                    "test_value": None,
                                    "test_dec": None},
                                    index=[0])
            test_stats = pd.concat([test_stats, test], axis=0)
            p = pd.DataFrame({"p_comp": None,
                                "p_value": None,
                                "p_dec": None},
                                index=[0])
            pvals = pd.concat([pvals, p], axis=0)
            continue

        # extract degrees of freedom
        try:
            dfs = extract_df(nhst_raw[i], test_type[i])

            # extract test comparison and test value

            test = extract_test_stats(nhst_raw[i])

            # extract p-comparison and p-value

            p = extract_p_value(nhst_raw[i])

        except:
            test_type[-1] = "None"
            print("Failed to read results for: " + nhst_raw[i])
            print("In the following text: " + str(name))
            dfs = pd.DataFrame({"df1": None,
                                "df2": None},
                                index=[0])
            test = pd.DataFrame({"test_comp": None,
                                    "test_value": None,
                                    "test_dec": None},
                                    index=[0])
            p = pd.DataFrame({"p_comp": None,
                                "p_value": None,
                                "p_dec": None},
                                index=[0])
        iteration_list = ["df1", "df2", "p"]
        for column_name in iteration_list:
            try:
                # try to round to 0 decimal places
                dfs[column_name][0] = float(dfs[column_name][0])
            except:
                pass


        df_result = pd.concat([df_result, dfs], axis=0)
        test_stats = pd.concat([test_stats, test], axis=0)
        pvals = pd.concat([pvals, p], axis=0)

    # create final data frame ------------------------------------------------------

    nhst_parsed = pd.DataFrame({
        # return raw result without leading/trailing whitespaces
        "Raw": [x.strip() for x in nhst_raw],
        "Statistic": test_type,
        "df1": df_result["df1"],
        "df2": df_result["df2"],
        "Test_Comparison": test_stats["test_comp"],
        "Value": test_stats["test_value"],
        "test_dec": test_stats["test_dec"],
        "Reported_Comparison": pvals["p_comp"],
        "Reported_P_Value": pvals["p_value"],
        "dec": pvals["p_dec"]
    })
    # drop None from test_type
    nhst_parsed = nhst_parsed[nhst_parsed["Statistic"] != "None"]

    if len(nhst_parsed) == 0:
        return pd.DataFrame()

    if len(nhst_parsed) > 0:

        # remove p values greater than one
        nhst_parsed["Reported_P_Value"] = [float(p) for p in nhst_parsed["Reported_P_Value"]]
        nhst_parsed = nhst_parsed[(nhst_parsed["Reported_P_Value"] <= 1) |
                                  nhst_parsed["Reported_P_Value"].isnull()]

        # remove correlations greater than one or smaller than -1
        # reason: there is a risk that statcheck simply misread this stat
        # this means that statcheck will not flag such incorrect correlations,
        # which you could also consider a disadvantage
        nhst_parsed['Value'] = [float(v) for v in nhst_parsed['Value']]
        nhst_parsed = nhst_parsed[~((nhst_parsed["Statistic"] == "r") &
                                    ((nhst_parsed["Value"] > 1) |
                                     (nhst_parsed["Value"] < -1)))]

        # remove rows with missing test values
        # reason: this can happen when a test statistic has a weird minus and a
        # space in front of it. statcheck can't convert the weird minus in that case
        # and would otherwise break down
        nhst_parsed = nhst_parsed[~nhst_parsed["Value"].isnull()]

        # only return selected stats
        # to that end, rename test-types to match argument stat
        types = nhst_parsed["Statistic"].values

        types[types == "r"] = "r"
        types[types == "Chi2"] = "Chi2"
        types[types == "Z"] = "Z"
        types[types == "Qw"] = "Q"
        types[types == "Qb"] = "Q"
        nhst_parsed["Statistic"] = types

        # only return rows where the test_type matches the selected stats
        nhst_parsed = nhst_parsed[nhst_parsed["Statistic"].isin(stat)]

        # nhst_parsed.__class__ = ("statcheck", "data.frame") # deleted because I am not sure if even necessary

        return nhst_parsed


