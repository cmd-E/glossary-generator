from pathlib import Path
import sys
from terms_loader import load_terms, sample_terms
from terms_exporter import export_txt, export_docx

def main():
    while True:
        try:
            count = int(input("Количество терминов (1-500): "))
            if 1 <= count <= 500:
                break
        except ValueError:
            pass
    while True:
        language = input("Язык(РУС/каз): ").strip().lower() or "рус"
        if language in ("рус", "каз"):
            break
    directory = Path(__file__).resolve().parent / "docs"
    try:
        terms = sample_terms(load_terms(language, directory / "terms_origin.html"), count)
        print(f"Сохранено: {export_txt(terms, language, directory)}")
        print(f"Сохранено: {export_docx(terms, language, directory)}")
    except Exception as error:
        print(f"Не удалось создать глоссарий: {error}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
