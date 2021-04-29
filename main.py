from app_config import AppConfig
from terms_loader import TermsLoader
from terms_exporter import TermsExporter


def main():
    terms_count = -1
    lang = "-"
    while terms_count < 1 or terms_count > 500:
        try:
            terms_count = int(input("Колличество терминов (1-500): "))
        except ValueError:
            continue
    while lang.lower() != "рус" and lang.lower() != "каз":
        lang = input("Язык(РУС/каз): ")
        if lang.strip() == "":
            lang = "рус"
    AppConfig.lang = lang
    AppConfig.terms_count = terms_count
    selected_terms = TermsLoader.get_terms()
    TermsExporter.export_terms_to_txt(selected_terms, AppConfig.lang)
    TermsExporter.doc_export(selected_terms, AppConfig.lang)


if __name__ == "__main__":
    main()
