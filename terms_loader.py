"""Load, validate and sample structured glossary data."""
from dataclasses import dataclass
from pathlib import Path
import random
import tempfile
import os

SOURCE_URL = "https://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm"
MAX_DOWNLOAD = 5 * 1024 * 1024

@dataclass(frozen=True)
class Term:
    name: str
    description: str

def parse_terms(html, language):
    from bs4 import BeautifulSoup
    column = {"рус": 0, "каз": 1}.get(language.lower())
    if column is None:
        raise ValueError("Неизвестный язык")
    table = BeautifulSoup(html, "html.parser").find("table")
    if table is None:
        raise ValueError("Таблица терминов не найдена")
    rows = table.find_all("tr")[1:]
    if not rows or len(rows) % 2:
        raise ValueError("Неполная таблица терминов")
    terms = []
    for index in range(0, len(rows), 2):
        pair = []
        for row in rows[index:index + 2]:
            cells = row.find_all("td")
            if len(cells) <= column:
                raise ValueError(f"Отсутствует перевод в строке {index + 2}")
            text = cells[column].get_text(" ", strip=True)
            if not text:
                raise ValueError(f"Пустая ячейка в строке {index + 2}")
            pair.append(text)
        terms.append(Term(*pair))
    return list(dict.fromkeys(terms))

def sample_terms(terms, count, rng=None):
    population = list(dict.fromkeys(terms))
    if not 1 <= count <= len(population):
        raise ValueError(f"Доступно уникальных терминов: {len(population)}")
    return (rng or random).sample(population, count)

def load_terms(language, cache_path, session=None):
    cache = Path(cache_path)
    if cache.is_file():
        try:
            return parse_terms(cache.read_text(encoding="utf-8"), language)
        except (ValueError, UnicodeError):
            pass
    if session is None:
        import requests
        session = requests
    client = session
    cache.parent.mkdir(parents=True, exist_ok=True)
    with client.get(SOURCE_URL, stream=True, timeout=(5, 20)) as response:
        response.raise_for_status()
        if not response.url.lower().startswith("https://") or any(
                not hop.url.lower().startswith("https://") for hop in response.history):
            raise ValueError("Источник перенаправил запрос на незащищенный HTTP")
        data = bytearray()
        for chunk in response.iter_content(8192):
            data.extend(chunk)
            if len(data) > MAX_DOWNLOAD:
                raise ValueError("Ответ источника слишком большой")
    text = data.decode("utf-8")
    terms = parse_terms(text, language)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=cache.parent,
                                         delete=False) as output:
            temporary = output.name
            output.write(text)
        os.replace(temporary, cache)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    return terms
