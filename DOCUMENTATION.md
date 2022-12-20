
<!-- README.md is generated from README.Rmd. Please edit that file -->
<!-- after editing README.Rmd, run devtools::build_readme() -->

# Documentation

This is a base documentation of the python version of the statcheck package. For more information,  
please refer to the documentation of the R version of the package: 

## Installation
```bash
pip install statcheck
```

## Analysis

You can analyze statistical analyzes using statcheck in two ways:

- Using the `statcheck` function on raw text
- Using the `checkdir` function on a directory of PDF or HTML files

### Using the `statcheck` function on raw text
```python
from statcheck.st import statcheck

text ='t(110.23) = 2.5,p= 0.013'

Res, pRes = statcheck(text)
```

### Using the `checkdir` function on a directory of PDF or HTML files
```python
from statcheck.checkdir import checkdir

dir = `C:/Users/username/Documents/MyPapers`

Res, pRes = checkdir(dir)
```

The `statcheck` function has the following arguments, they can be passed to the checkdir function as well: 
- `x`: a string containing the text to be analyzed, or a list of strings
- `stat` : The type of statistical test to be checked.
  - (default = ["t", "F", "cor", "chisq", "Z"])
- `OneTailedTests`: Defines whether we treat all extracted tests as two-tailed.
  - (default = False)
- `alpha`: Defines which level of significance statcheck will assume.
  - (default: 0.05)
- `pEqualAlphaSig`: Defines whether a p-value equal to α is treated as significant.
  - (default: True)
- `pZeroError`: Controls whether statcheck will count a p-value reported as “p=.000” as an error.
  - (default: True)
- `OneTailedTxt`: Controls whether statcheck will try to identify and correct for one-tailed tests.
  - (default: False)
- `AllPValues`:  If you set the argument AllPValues to TRUE, statcheck will only search for p-values
  - (default: False)
- `messages`: Whether to print messages to the console.
  - (default: True)
- `names`: A vector of names for the results. If no names are provided, the results will be named 0, 1, 2, etc.  
  If PDF or HTML files are analyzed, the names will be inherited from file names
  - (default: None)

## Output

The output of the `statcheck` function is two pandas dataframes: Res, and pRes.

- Res contains the results of the statistical analysis
  - columns:
    - `Source` - The source of the text.
    - `Statistic` - The type of statistical test.
    - `df1` - The degrees of freedom of the first sample.
    - `df2` - The degrees of freedom of the second sample.
    - `Test_Comparison` - The comparison of the test (e.g. `=`).
    - `Value` - The value of the test statistic.
    - `Reported_P_Comparison` - The comparison of the p-value (e.g. `<`).
    - `Reported_P_Value` - The reported p-value.
    - `Computed` - The computed p-value.
    - `Raw` - The raw text of the statistical analysis (e.g. `t(110.23) = 2.5,p= 0.013`).
    - `Error` - Whether there is an error in the statistical analysis.
    - `DecisionError` - Whether there is an error in the significance decision.
    - `OneTailedInTxt` - Whether the test is one-tailed in the text.
    - `APAfactor` - The assigned APA factor.


- pRes contains the extracted p-values
    - columns
      - `p_comp` - The comparison of the p-value (e.g. `<`).
      - `p_value` - The value of the p statistic.
      - `p_dec` - The number of decimals in the p-value.
      - `Source` - The source of the text.


### Statistical Checks Summary
The summary of the statistical checks can be generated using the summary_statcheck function.
The result is a dataframe with the following columns:
- `Source` - The source of the text.
- `pValues` - The number of p-values.
- `Errors` - The number of errors in the statistical analysis.
- `DecisionErrors` - The number of errors in the significance decision.

```python
from statcheck.st import statcheck
from statcheck.sum_st import summary_statcheck

text ='t(110.23) = 2.5,p= 0.013'

Res, pRes = statcheck(text)

summary = summary_statcheck(Res)
```

### Plotting the results
The summary of the statistical checks can be generated using the summary_statcheck function. The APA version  
of the plot is not available in the python version of the package.

```python
from statcheck.st import statcheck
from statcheck.plot_statcheck import plot_statcheck

text ='t(110.23) = 2.5,p= 0.013'

Res, pRes = statcheck(text)
                      
plot_statcheck(Res)
```

## Tests
To run the tests of the package, clone the repository and run the following commands in the terminal:
```bash
pip install pytest
pytest tests/
```

