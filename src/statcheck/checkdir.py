from file_to_txt import getPDF, getHTML
from statcheck import statcheck


import os
from tkinter import filedialog, ttk

def checkdir(dir = None, subdir = True, *args):
    if dir is None:
        root = ttk()
        root.withdraw()
        files = filedialog.askopenfilenames()

    pdfs = any(re.search(r"\.pdf$", file, re.IGNORECASE) for file in os.listdir(dir))
    htmls = any(re.search(r"\.html?$", file, re.IGNORECASE) for file in os.listdir(dir))

    if pdfs:
        pdfres = checkPDFdir(dir, subdir, *args)
    if htmls:
        htmlres = checkHTMLdir(dir, subdir, *args)

    if pdfs and htmls:
        if pdfres is not None and htmlres is not None:
            res = pd.concat([pdfres, htmlres])
        else:
            raise ValueError("statcheck did not find any results")
    elif pdfs and not htmls:
        if pdfres is not None:
          res = pdfres
        else:
          raise ValueError("statcheck did not find any results")
    elif not pdfs and htmls:
        if htmlres is not None:
            res = htmlres
        else:
            raise ValueError("statcheck did not find any results")
    elif not pdfs and not htmls:
        raise ValueError("No PDF or HTML found")

    res.__class__ = "statcheck", "data.frame"
    return res


############# HTML CHECKING FUNCTIONS #############
def checkHTML(files=None, *args, **kwargs):
    if files is None:
        root = ttk()
        root.withdraw()
        files = filedialog.askopenfilenames()

    texts = getHTML(files)

    names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return statcheck(texts, names = names)

def checkHTMLdir(dir=None, subdir=True, extension=True, *args, **kwargs):
    if dir is None:
        root = ttk()
        root.withdraw()
        files = filedialog.askopenfilenames()
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
    return statcheck(texts, names = names)



############# PDF CHECKING FUNCTIONS #############
def checkPDF(files=None, *args, **kwargs):
    if files is None:
        root = Tk()
        root.withdraw()
        files = filedialog.askopenfilenames()


    names = [os.path.splitext(os.path.basename(file))[0] for file in files]
    return statcheck(texts, names = names)


def checkPDFdir(dir=None, subdir=True, *args, **kwargs):
    if dir is None:
        root = ttk()
        root.withdraw()
        files = filedialog.askopenfilenames()

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
    return statcheck(texts, names = names)