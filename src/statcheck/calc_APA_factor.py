def calc_APA_factor(Res, pRes):
  # select only the results of pRes that are from articles with at least 1 statcheck result
  pRes_selection = pRes[pRes['Source'].isin(Res['Source'])]

  # Source should not be a factor. This would result in a bug down the road, if
  # one of the sources didn't have any APA results:
  # Error in by(Res_selection, Res_selection$Source, nrow)/by(pRes_selection,  :
  # non-conformable arrays
  pRes_selection['Source'] = pRes_selection['Source'].tolist()

  # select only the statcheck results that are from an article with at least one p value
  # this is relevant, because it sometimes happens that statcheck extracts less p values
  # p values than statcheck results. For instance in cases when a p value appears to be
  # greater than 1.

  Res_selection = Res[Res['Source'].isin(pRes_selection['Source'])]

  # Calculate APA factor
  APA = Res_selection.groupby('Source').size() / pRes_selection.groupby('Source').size()

  APAfactor = APA[Res['Source']].round(2).tolist()

  return APAfactor
