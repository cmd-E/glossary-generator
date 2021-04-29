import os.path
import random
import sys
import requests
from bs4 import BeautifulSoup
from app_config import AppConfig
from tqdm import tqdm


class TermsLoader:
    @classmethod
    def get_terms(cls) -> list:
        """Loads terms from url, parses it, and returns 'terms_count' random terms"""
        raw_terms = cls.__load_raw_terms()
        terms_list = cls.__parse_terms(raw_terms, AppConfig.lang)
        selected_terms = cls.__get_random_terms(terms_list)
        return selected_terms

    @staticmethod
    def __load_raw_terms() -> list:
        url = "http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"
        html_filename = 'terms_origin.html'
        if not os.path.isfile(html_filename):
            print('Загрузка терминов...')
            try:
                response = requests.get(url, stream=True)
                total_size_in_bytes = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 Kibibyte
                progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
                with open(html_filename, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                progress_bar.close()
                if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                    print("ERROR, something went wrong")
            except:
                print("Unexpected error occurred while getting response from glossary page: ",
                      sys.exc_info()[0])
                exit()
        soup = ""
        try:
            with open(html_filename, 'r', encoding="utf-8") as file:
                content = file.read()
            soup = BeautifulSoup(content, "html.parser")
        except:
            print("Unexpected error occurred while parsing response from glossary page: ",
                  sys.exc_info()[0])
        print("Парсинг терминов...")
        trs = soup.find("table").find_all("tr")
        trs = trs[1:]
        return trs

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
