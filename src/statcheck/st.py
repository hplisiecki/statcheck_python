from st.helpers_parse_stats import extract_p_value
from st.extract_stats import extract_stats
from st.extract_1tail import extract_1tail
from st.calc_APA_factor import calc_APA_factor
from st.process_stats import process_stats

import pandas as pd
pd.options.mode.chained_assignment = None
from tqdm import tqdm


def statcheck(texts, stat=["t", "F", "r", "Chi2", "Z", "Q"],
              OneTailedTests=False, alpha=.05, pEqualAlphaSig=True,
              pZeroError=True, OneTailedTxt=False,
              messages=True, names = None):

    # check if texts is a list
    if type(texts) != list:
        texts = [texts]
    # We need empty data frames to store extracted statistics in
    # One for NHST results (Res) and one for p-values (pRes)
    Res = pd.DataFrame()
    pRes = pd.DataFrame()

    # to indicate where the statistics came from, we need a name for the input
    # texts. In some cases, this is the name of the file the text came from, but
    # if the text has no name, number them
    if names is None:
        names_dict = {texts[i]: i for i in range(len(texts))}
    else:
        names_dict = {texts[i]: names[i] for i in range(len(texts))}
    print("Extracting statistics from text")
    for txt in tqdm(names_dict.keys()):


        # extract p-values ------------------------------------------

        # extract all p values. This is based on a pretty rough regular expression
        # that will extract anything that resembles p =<> .... We need this info
        # later on to calculate the APA factor: the ratio (statcheck results)/
        # (total # of p values). It is also possible to let statcheck return this
        # dataframe instead of the data frame with NHST results.
        p_values = extract_p_value(txt)

        # append and close:
        # in each repetition of the loop, the extracted p-values are appended
        # to the existing pRes data frame, so it grows in each step
        if len(p_values) > 0:
            p_values['Source'] = [names_dict[txt] for j in range(len(p_values))]
            pRes = pd.concat([pRes, p_values], ignore_index=True)

        # after appending the pvalues dataframe to the main pRes dataframe,
        # the temporary dataframe pvalues can be removed.
        del p_values

        # extract NHST results ------------------------------------------

        # extract all NHST results. This function scrapes the text for all APA
        # reported NHST results and parses it so that the separate elements are
        # returned in one large dataframe
        nhst = extract_stats(txt=txt,
                               stat=stat,
                               name=names_dict[txt])

        # append and close: same logic as for the pvalues dataframe above
        if len(nhst) > 0:
            nhst['Source'] = [names_dict[txt] for j in range(len(nhst))]
            nhst['OneTailedInTxT'] = [extract_1tail(txt) for j in range(len(nhst))] # IDK

            Res = pd.concat([Res, nhst], ignore_index=True)
            Res = Res.reset_index(drop=True)

        del nhst
        print()
    if messages:
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=")
        print(" Done extracting statistics")
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=")



    if len(Res) > 0:
        # If the argument OneTailedTests == TRUE, it forces statcheck to treat
        # every encountered NHST result as a one-tailed test. Note: this is not the
        # same as the automated 1-tailed test detection (switched on with the
        # argument: OneTailedTxt). The latter works more subtly (see comments in
        # process_stats()).

        if OneTailedTests:
            two_tailed = False
        else:
            two_tailed = True

        # create empty variables to fill out during the loop
        computed_list = []
        error_list = []
        decision_error = []

        # row by row, process the extracted statistics in Res. Specifically,
        # compute the p-value, check if the result is an error and a decision error,
        # and if indicated in the options, check & correct for 1-tailed tests
        old_name = None

        for i in tqdm(Res.index):

            result = process_stats(Res['Statistic'][i],
                                   test_stat = Res['Value'][i],
                                   df1 = Res['df1'][i],
                                   df2 = Res['df2'][i],
                                   reported_p = Res['Reported_P_Value'][i],
                                   p_comparison = Res['Reported_Comparison'][i],
                                   test_comparison = Res['Test_Comparison'][i],
                                   p_dec = Res['dec'][i],
                                   test_dec = Res['test_dec'][i],
                                   OneTailedInTxt = Res['OneTailedInTxT'][i],
                                   two_tailed = two_tailed,
                                   alpha = alpha,
                                   pZeroError = pZeroError,
                                   pEqualAlphaSig = pEqualAlphaSig,
                                   OneTailedTxt = OneTailedTxt,
                                   OneTailedTests = OneTailedTests)

            computed_list.append(result['computed_p'].iloc[0])
            error_list.append(result['error'].iloc[0])
            decision_error.append(result['decision_error'].iloc[0])

        Res['Computed'] = computed_list
        Res['Error'] = error_list
        Res['Decision_Error'] = decision_error
        ###---------------------------------------------------------------------

        # APAfactor: proportion of APA results (that statcheck reads)
        # in total number of p values

        Res['APAfactor'] = calc_APA_factor(Res, pRes)

        ###---------------------------------------------------------------------

        # select & reorder columns for final data frame
        Res = Res[["Source", "Statistic", "df1", "df2", "Test_Comparison",
                    "Value", "Reported_Comparison", "Reported_P_Value",
                    "Computed", "Raw", "Error", "Decision_Error",
                    "OneTailedInTxT", "APAfactor"]]


        Res.columns = ["Source", "Statistic", "df1", "df2", "Test_Comparison",
                       "Value", "Reported_P_Comparison", "Reported_P_Value",
                       "Computed", "Raw", "Error", "DecisionError",
                       "OneTailedInTxt", "APAfactor"]

        # Return ------------------------------------------------------------------


    else:
        if len(pRes) > 0:
            # rename columns based on the variable names in the script constants.R
            # first make sure that the columns are in the right order before renaming

            pRes = pRes[["Source", "p_comp", "p_value", "p_dec"]]
            pRes.columns = ["Source", "Reported_P_Comparison", "Reported_P_Value", "P_Value_Decimals"]

        else:
            print("No p values found")

    if messages:
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=")
        print(" Done processing statistics")
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=")

    return Res, pRes