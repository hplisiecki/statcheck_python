# template for the statcheck_report script


def statcheckReport(Res, pRes, filename, directory):

    # save Res and pRes to csv files
    Res.to_csv(os.path.join(directory, filename + "_Res.csv"))
    pRes.to_csv(os.path.join(directory, filename + "_pRes.csv"))