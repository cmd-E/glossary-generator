import requests
from bs4 import BeautifulSoup
import time
url = "http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
trs = soup.find("table").find_all("tr")
i = 0
file = open("glossary.txt", "w", encoding="UTF-8")
description = ""
term = ""
for tr in trs[1:]:
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
        line = f"{term} - {description}\r"
        file.write(line)
        term = ""
        description = ""
        i += 1
file.close()
