from app_config import AppConfig
from terms_loader import TermsLoader
from terms_exporter import TermsExporter


def main():
    AppConfig.terms_count = -1
    AppConfig.lang = "-"
    while AppConfig.terms_count == -1:
        AppConfig.terms_count = int(input("Колличество терминов: "))
        if AppConfig.terms_count >= 502 or AppConfig.terms_count < 1:
            print("Таблица содержит 502 термина и колиичество терминов не может быть меньше 1")
            AppConfig.terms_count = -1
    while AppConfig.lang == "-":
        AppConfig.lang = input("Язык(РУС/каз): ")
        if AppConfig.lang.strip() == "":
            AppConfig.lang = "рус"
        elif AppConfig.lang.lower() != "рус" and AppConfig.lang.lower() != "каз":
            AppConfig.lang = "-"
    selected_terms = TermsLoader.get_terms()
    TermsExporter.export_terms_to_txt(selected_terms, AppConfig.lang)
    TermsExporter.doc_export(selected_terms, AppConfig.lang)


if __name__ == "__main__":
    main()
