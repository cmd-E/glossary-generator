import requests
from bs4 import BeautifulSoup
import random
import docx
import sys


def getTerms():
    description = ""
    term = ""
    termsList = []
    j = 0
    for tr in trs:
        if j % 2 != 0:
            if lang.lower() == "рус":
                description = tr.find("td").find("p").getText()
                description = description.replace("\r", "")
                description = description.replace("\n", "")
            else:
                description = tr.find_all("td")[1].find("p").getText()
                description = description.replace("\r", "")
                description = description.replace("\n", "")
        else:
            if lang.lower() == "рус":
                term = tr.find("td").find("p").getText()
                term = term.replace("\r", "")
                term = term.replace("\n", "")
            else:
                term = tr.find_all("td")[1].find("p").getText()
                term = term.replace("\r", "")
                term = term.replace("\n", "")
        if term == "" or description == "":
            j += 1
            continue
        else:
            termsList.append([
                term, description
            ])
            term = ""
            description = ""
            j += 1
    return termsList


used = []


def getRandomTerm(termsList):
    line = ""
    term = ""
    randomTerm = random.randint(0, len(termsList) - 1)
    if randomTerm not in used:
        term = termsList[randomTerm]
        line = f"{term[0]} - {term[1]}\n"
        used.append(randomTerm)
    else:
        line = getRandomTerm(termsList)
    return line


def docExport(terms):
    for i in range(len(terms)):
        terms[i] = terms[i].split(" - ", 1)
    doc = docx.Document()
    doc.add_heading("Глоссарий", 0)
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    hdr_Cells = table.rows[0].cells
    if lang.lower() == "рус":
        hdr_Cells[0].text = "Термин"
        hdr_Cells[1].text = "Значение"
    else:
        hdr_Cells[0].text = "Термин"
        hdr_Cells[1].text = "Терминнің мағынасы"
    try:
        i = 0
        for term, description in terms:
            row_Cells = table.add_row().cells
            row_Cells[0].text = term
            row_Cells[1].text = description
            i += 1
    except:
        print(f"Exception occured: {sys.exc_info()[0]}")
        print(f"Term: {term} Description: {description} I: {i}")
        print(terms[i])
    filename = ""
    if lang.lower() == "рус":
        filename = "glossary_ru.docx"
    else:
        filename = "glossary_kz.docx"
    doc.save(filename)


url = "http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"
termsCount = -1
lang = "-"
while termsCount == -1:
    termsCount = int(input("Колличество терминов: "))
    if termsCount >= 502:
        print("Таблица содержит 502 термина")
        termsCount = -1
while lang == "-":
    lang = input("Язык(РУС/каз): ")
    if lang == "":
        lang = "рус"
    elif lang.lower() != "рус" and lang.lower() != "каз":
        lang = "-"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
trs = soup.find("table").find_all("tr")
trs = trs[1:]
termsList = getTerms()

termsForExport = []
filename = ""
if lang.lower() == "рус":
    filename = "glossary_ru.txt"
else:
    filename = "glossary_kz.txt"
with open(filename, "w", encoding="UTF-8") as glossaryFile:
    for i in range(termsCount):
        tempTerm = getRandomTerm(termsList)
        glossaryFile.write(tempTerm)
        termsForExport.append(tempTerm)

docExport(termsForExport)
