# glossary-generator
Создает глоссарий с терминами в формате `.txt` и таблицей в `.docx` на русском и казахском языках

Берет информацию из http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm (500 терминов)

# Использование
- Запустить `main.py` из коммандной строки
- Задать необходимое колличество терминов
- Выбрать язык
- Забрать термины из `glossary.txt` (находится в директории с `main.py`)

# Зависимости
`requests`, `BeautifulSoup`, `python-docx`

Установить всё: `py -m pip install -r requirements.txt`