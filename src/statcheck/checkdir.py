from statcheck.file_to_txt import getPDF, getHTML
from statcheck.st import statcheck

import re
import os

def checkdir(dir, subdir = True, *kwargs):
    """
    Check all files in a directory for statistical errors.
    :param dir: Directory to check
    :param subdir: Check subdirectories
    :param kwargs: Keyword arguments for statcheck
    :return: Results of statcheck
    """
    pdfs = any(re.search(r"\.pdf$", file, re.IGNORECASE) for file in os.listdir(dir))
    htmls = any(re.search(r"\.html?$", file, re.IGNORECASE) for file in os.listdir(dir))

    if pdfs:
        pdfres, pdfPres = checkPDFdir(dir, subdir, *kwargs)
    if htmls:
        htmlres, pdfPres = checkHTMLdir(dir, subdir, *kwargs)

    if pdfs and htmls:
        if pdfres is not None and htmlres is not None:
            res = pd.concat([pdfres, htmlres])
            pres = pd.concat([pdfPres, htmlPres])
        else:
            raise ValueError("statcheck did not find any results")
    elif pdfs and not htmls:
        if pdfres is not None:
          res = pdfres
          pres = pdfPres
        else:
          raise ValueError("statcheck did not find any results")
    elif not pdfs and htmls:
        if htmlres is not None:
            res = htmlres
            pres = htmlPres
        else:
            raise ValueError("statcheck did not find any results")
    elif not pdfs and not htmls:
        raise ValueError("No PDF or HTML found")

    return res, pres


############# HTML CHECKING FUNCTIONS #############
def checkHTML(files, **kwargs):
    """
    Check a list of HTML files for statistical errors.
    :param files: List of HTML files
    :param kwargs: Keyword arguments for statcheck
    :return: Results of statcheck
    """
    texts = getHTML(files)

    names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return statcheck(texts, names = names, *kwargs)

def checkHTMLdir(dir, subdir=True, extension=True, **kwargs):
    """
    Check all HTML files in a directory for statistical errors.
    :param dir: Directory to check
    :param subdir: Check subdirectories
    :param extension: Check file extension
    :param kwargs: Keyword arguments for statcheck
    :return: Results of statcheck
    """
    if extension:
        pat = ".html|.htm"
    else:
        pat = ""

    files = []
    if subdir:
        for path, _, filenames in os.walk(dir):
            for filename in filenames:
                if re.search(pat, filename):
                    files.append(os.path.join(path, filename))
    else:
        for filename in os.listdir(dir):
            if re.search(pat, filename):
                files.append(os.path.join(dir, filename))

    if not files:
        raise ValueError("No HTML files found")

    texts = getHTML(files)

    names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return statcheck(texts, names = names, *kwargs)



############# PDF CHECKING FUNCTIONS #############
def checkPDF(files=None, **kwargs):
    """
    Check a list of PDF files for statistical errors.
    :param files: List of PDF files
    :param kwargs: Keyword arguments for statcheck
    :return: Results of statcheck
    """
    texts = getPDF(files)

    names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return statcheck(texts, names = names, *kwargs)


def checkPDFdir(dir, subdir=True, **kwargs):
    """
    Check all PDF files in a directory for statistical errors.
    :param dir: Directory to check
    :param subdir: Check subdirectories
    :param kwargs: Keyword arguments for statcheck
    :return: Results of statcheck
    """
    files = []
    if subdir:
        for path, _, filenames in os.walk(dir):
            for filename in filenames:
                if filename.endswith(".pdf"):
                    files.append(os.path.join(path, filename))
    else:
        for filename in os.listdir(dir):
            if filename.endswith(".pdf"):
                files.append(os.path.join(dir, filename))

    if not files:
        raise ValueError("No PDF files found")

    print("Importing PDF files...")
    texts = getPDF(files)

    names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return statcheck(texts, names = names, *kwargs)