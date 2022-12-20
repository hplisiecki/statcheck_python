def identify_statcheck(x, alpha=0.05, **kwargs):
    # Get the 'reported' and 'computed' columns from the data frame
    reported = x[VAR_REPORTED_P]
    computed = x[VAR_COMPUTED_P]

    # Replace 'ns' values with the given alpha value
    x.loc[x[VAR_P_COMPARISON] == "ns", VAR_REPORTED_P] = alpha

    # Call the plot.statcheck() function, passing any additional arguments
    plot.statcheck(x, APAstyle=False, **kwargs)

    # Identify points in the plot
    ID = graphics.identify(reported, computed)

    # Subset the data frame to include only the identified points
    res = x.loc[ID]

    # Set the class of the resulting data frame
    res.__class__ = ("statcheck", "data.frame")

    return res
