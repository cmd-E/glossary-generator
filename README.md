# glossary-generator
Создает глоссарий с терминами в формате `.txt` и таблицей в `.docx`

Берет информацию из http://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm (500 терминов на русском языке)

# Использование
- Запустить `parser.py` из коммандной строки или `parser.exe`
- Задать необходимое колличество терминов
- Забрать термины из `glossary.txt` (находится в директории с `parser.py`)

# Зависимости
`requests` - `pip install requests`

`BeautifulSoup` - `pip install beautifulsoup4`

 `python-docx` - `pip install python-docx`
