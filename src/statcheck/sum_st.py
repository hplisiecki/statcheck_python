import pandas as pd
# suppress pandas warnings
pd.options.mode.chained_assignment = None
def summary_statcheck(Res):
    """
    Summarizes the results of statcheck
    :param Res: output of statcheck
    :return: summary of results
    """

    # Source
    source = list(Res['Source'].unique())
    source.append("Total")

    # groupby Source
    p_values = Res.groupby('Source').count()
    p_values = list(p_values['Reported_P_Value'].values)
    p_values.append(len(Res))

    # Number of errors per article and in total
    errors = Res.groupby('Source').sum()
    errors = list(errors['Error'].values)
    errors.append(sum(errors))

    # Number of decision errors per article and in total
    decision_errors = Res.groupby('Source').sum()
    decision_errors = list(decision_errors['DecisionError'].values)
    decision_errors.append(sum(decision_errors))

    # Results in dataframe
    res = pd.DataFrame(
        {
            "Source": source,
            "pValues": p_values,
            "Errors": errors,
            "DecisionErrors": decision_errors
        }
    )

    # Rename columns based on constants in constants.R file
    res.columns = ['Source', 'pValues', 'Errors', 'DecisionErrors']

    return res