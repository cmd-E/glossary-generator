import random
import sys

import requests
from bs4 import BeautifulSoup

from app_config import AppConfig


class TermsLoader:
    @classmethod
    def get_terms(cls) -> list:
        raw_terms = cls.__load_raw_terms()
        terms_list = cls.__parse_terms(raw_terms, AppConfig.lang)
        selected_terms = cls.__get_random_terms(terms_list)
        return selected_terms

    @classmethod
    def __parse_terms(cls, raw_terms: list, lang: str) -> list:
        description = ""
        term = ""
        terms_list = []
        j = 0
        for tr in raw_terms:
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
                terms_list.append([
                    term, description
                ])
                term = ""
                description = ""
                j += 1
        return terms_list

    @classmethod
    def __get_random_terms(cls, terms_list: list) -> list:
        used_terms = []
        selected_terms = []
        for i in range(AppConfig.terms_count):
            random_term = terms_list[random.randint(0, len(terms_list) - 1)]
            formatted_term = f"{random_term[0]} - {random_term[1]}\n"
            if formatted_term not in used_terms:
                selected_terms.append(formatted_term)
                used_terms.append(formatted_term)
            else:
                AppConfig.terms_count += 1
                continue
        return selected_terms

    @staticmethod
    def __load_raw_terms() -> list:
        url = "http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"
        response = ""
        try:
            response = requests.get(url)
        except:
            print("Unexpected error occurred while getting response from glossary page: ",
                  sys.exc_info()[0])
            exit()

        soup = ""
        try:
            soup = BeautifulSoup(response.content, "html.parser")
        except:
            print("Unexpected error occurred while parsing response from glossary page: ",
                  sys.exc_info()[0])

        trs = soup.find("table").find_all("tr")
        trs = trs[1:]
        return trs
