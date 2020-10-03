import requests
from bs4 import BeautifulSoup
import random
url = "http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"

termsCount = int(input("Колличество терминов: "))
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
trs = soup.find("table").find_all("tr")
trs = trs[1:]
i = 0
description = ""
term = ""
termsList = []
for tr in trs:
    if i % 2 != 0:
        description = tr.find("td").find("p").getText()
        description = description.replace("\r", "")
        description = description.replace("\n", "")
    else:
        term = tr.find("td").find("p").getText()
        term = term.replace("\r", "")
        term = term.replace("\n", "")
    if term == "" or description == "":
        i += 1
        continue
    else:
        # line = f"{term} - {description}\r"
        termsList.append([
            term, description
        ])
        term = ""
        description = ""
used = []
glossaryFile = open("glossary.txt", "w", encoding="UTF-8")
i = 0
while i < termsCount:
    randomTerm = random.randint(0, len(termsList))
    if randomTerm not in used:
        term = termsList[randomTerm]
        glossaryFile.write(f"{term[0]} - {term[1]}\n")
        used.append(randomTerm)
        i += 1
glossaryFile.close()
