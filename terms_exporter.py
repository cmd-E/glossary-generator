"""Export structured terms without modifying the caller's data."""
from pathlib import Path
import os
import tempfile

def _destination(directory, language, suffix):
    code = {"рус": "ru", "каз": "kz"}.get(language.lower())
    if code is None:
        raise ValueError("Неизвестный язык")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"glossary_{code}.{suffix}"

def _save_atomic(destination, write):
    handle, temporary = tempfile.mkstemp(dir=destination.parent, suffix=destination.suffix)
    os.close(handle)
    try:
        write(temporary)
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return destination

def export_txt(terms, language, directory):
    content = "".join(f"{term.name} - {term.description}\n" for term in terms)
    return _save_atomic(_destination(directory, language, "txt"),
                        lambda path: Path(path).write_text(content, encoding="utf-8"))

def export_docx(terms, language, directory):
    import docx
    document = docx.Document()
    document.add_heading("Глоссарий", 0)
    table = document.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.rows[0].cells[0].text = "Термин"
    table.rows[0].cells[1].text = "Значение" if language.lower() == "рус" else "Терминнің мағынасы"
    for term in terms:
        cells = table.add_row().cells
        cells[0].text, cells[1].text = term.name, term.description
    return _save_atomic(_destination(directory, language, "docx"), document.save)
