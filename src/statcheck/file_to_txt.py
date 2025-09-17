from bs4 import BeautifulSoup
from tqdm import tqdm
import PyPDF2
import re

# HTML TO TXT ------------------------------------------------------------------


def getHTML(files):
    """
    Extracts the text from a list of HTML files.
    :param files: List of HTML files
    :return: List of text strings
    """
    if type(files) != list:
        files = [files]
    strings = []
    failed = []
    for file in tqdm(files):
        # open a html file
        try:
            with open(file, 'r', encoding='utf-8') as f:
                html = f.read()

            # parse the html file
            soup = BeautifulSoup(html)
            strings.append(soup.get_text())
        except:
            failed.append(file)
            continue

    # not sure if that is actually needed with soup, but does not hurt to add it:
    strings = [re.sub(r"<sub>(?!rep).*?</sub>", "", string) for string in strings]
    strings = [re.sub(r"<(.|\n)*?>", "", string) for string in strings]

    strings = [string.replace("&#60;", "<") for string in strings]
    strings = [string.replace("&lt;", "<") for string in strings]
    strings = [string.replace("&LT;", "<") for string in strings]
    strings = [string.replace("&#x0003C;", "<") for string in strings]
    strings = [string.replace("&#x0003c;", "<") for string in strings]

    strings = [string.replace("&#61;", "=") for string in strings]
    strings = [string.replace("&equals;", "=") for string in strings]
    strings = [string.replace("&#x0003D;", "=") for string in strings]

    strings = [string.replace("&#62;", ">") for string in strings]
    strings = [string.replace("&gt;", ">") for string in strings]
    strings = [string.replace("&GT;", ">") for string in strings]
    strings = [string.replace("&#x0003E;", ">") for string in strings]

    strings = [string.replace("&#40;", "(") for string in strings]
    strings = [string.replace("&#41;", ")") for string in strings]

    strings = [string.replace("&thinsp;", " ") for string in strings]
    strings = [string.replace("&nbsp;", " ") for string in strings]
    strings = [string.replace("\n", "") for string in strings]
    strings = [string.replace("\r", "") for string in strings]
    strings = [re.sub(r"\s+", " ", string) for string in strings]

    strings = [string.replace("&minus;", "-") for string in strings]
    strings = [string.replace("&#x02212;", "-") for string in strings]
    strings = [string.replace("&#8722;", "-") for string in strings]

    strings = [string.replace("&chi;", "X") for string in strings]
    strings = [string.replace("&#x003C7;", "X") for string in strings]
    strings = [string.replace("&#x003c7;", "X") for string in strings]
    strings = [string.replace("&#967;", "X") for string in strings]
    strings = [string.replace("&Chi;", "X") for string in strings]
    strings = [string.replace("&#x003A7;", "X") for string in strings]
    strings = [string.replace("&#935;", "X") for string in strings]

    print("Failed to convert: ", failed)

    return strings

# PDF TO TXT -------------------------------------------------------------------

def getPDF(files):
    """
    Extracts the text from a list of PDF files.
    :param files: List of PDF files
    :return: List of text strings
    """

    if type(files) != list:
        files = [files]
    failed = []
    strings = []
    for file in tqdm(files):
        try:
            pdfFileObj = open(file, 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj, strict=False)
            text = ""
            for page in range(len(pdfReader.pages)):
                text += pdfReader.pages[page].extract_text()

            # this code gets rid of XML artifacts
            raw_text = text.encode('unicode_escape').decode('utf-8')
            regex = r'\\x[0-9]{2}'
            modified_text = re.sub(regex, ' ', raw_text)
            modified_text = modified_text.encode('utf-8').decode('unicode_escape')
            strings.append(modified_text)
        except:
            failed.append(file)
            continue
    print("Failed to convert: ", failed)

    return strings
