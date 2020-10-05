import requests
from bs4 import BeautifulSoup
import random


def getTerms():
    description = ""
    term = ""
    termsList = []
    j = 0
    for tr in trs:
        if j == 300:
            print("Break")
        elif j == 400:
            print("Break")
        elif j == 490:
            print("Break")
        elif j == len(trs) - 50:
            print("Break")
        elif j == len(trs) - 5:
            print("Break")
        if j % 2 != 0:
            description = tr.find("td").find("p").getText()
            description = description.replace("\r", "")
            description = description.replace("\n", "")
        else:
            term = tr.find("td").find("p").getText()
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


url = "http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"
termsCount = -1
while termsCount == -1:
    termsCount = int(input("Колличество терминов: "))
    if termsCount >= 503:
        print("Таблица содержит 502 термина")
        termsCount = -1

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
trs = soup.find("table").find_all("tr")
trs = trs[1:]
i = 0
termsList = getTerms()


with open("glossary.txt", "w", encoding="UTF-8") as glossaryFile:
    for i in range(termsCount):
        glossaryFile.write(getRandomTerm(termsList))
