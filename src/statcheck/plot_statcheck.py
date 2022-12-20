import matplotlib.pyplot as plt
# placeholder for the plot_statcheck.py script

def plot_statcheck(x, alpha = 0.05):
    """
    Plot the results of statcheck.
    :param x: list of strings
    :param alpha: significance level
    """
    x.loc[x['Reported_P_Comparison'] == "ns", 'Reported_P_Comparison'] = ">"
    x.loc[x['Reported_P_Comparison'] == "ns", 'Reported_P_Value'] = alpha

    reported = x['Reported_P_Value'].values
    computed = x['Computed_P_Value'].values


    # scatterplot of reported and recalculated p values
    plt.scatter(reported, computed, marker='o', s = 20)

    plt.xlabel("reported p value")
    plt.ylabel("recalculated p value")

    # change color of points based on error so that errors will be orange
    # and correct results will be blue
    plt.scatter(reported[x['Reported_P_Comparison'] == "="],
            computed[x['Reported_P_Comparison'] == "="], marker='D', s = 20, color = 'blue')

    plt.scatter(reported[x['Error'] == 1], computed[x['Error'] == 1],
                marker='o', color='orange')
    plt.scatter(reported[x['Decision_Error'] == 1],
                computed[x['Decision_Error'] == 1], marker='o', color='red')

    plt.scatter(x['Reported_P_Value'][x['Reported_P_Comparison'] == "="],
                computed[x['Reported_P_Comparison'] == "="],
                marker='D')

    # general layout of figure:
    # lines & text to indicate under- and overestimates
    plt.axhline(y=0.05)
    plt.axvline(x=0.05)
    plt.plot([0, 1], [0, 1])

    plt.text(0.8, 0.4, "overestimated")
    plt.text(0.4, 0.8, "underestimated")

    plt.text(0, 0.53, "non-sig", fontsize=7)
    plt.text(0, 0.50, "reported", fontsize=7)
    plt.text(0, 0.47, "as sig", fontsize=7)

    plt.text(0.5, 0, "sig reported as non-sig", fontsize=7)

    plt.legend(['p inconsistency', 'decision error', 'exact (p = ...)'],
               loc='upper left',
               markerscale=0.8,
               scatterpoints=1)