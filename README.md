# glossary-generator

Создает глоссарий на русском или казахском языке в TXT и DOCX.

## Запуск

```
python -m pip install -r requirements.txt
python main.py
```

Введите количество терминов (1–500) и язык. Результаты сохраняются в папке docs рядом с main.py независимо от текущей рабочей директории. Если уникальных терминов недостаточно, программа сообщает доступное количество.

Источник: https://libr.aues.kz/facultet/frts/kaf_aes/52/umm/aes_1.htm.
Загрузка ограничена по времени и размеру. HTTP и переходы с HTTPS на HTTP запрещены.
Если источник недоступен, можно использовать ранее сохраненный валидный docs/terms_origin.html.
Неполный ответ или неверная таблица не заменяют кэш.

Парсер возвращает неизменяемые Term(name, description); выборка выполняется без повторений.
Экспортеры не меняют входные данные. Каждый файл сохраняется через временный файл;
TXT и DOCX завершаются независимо, и программа сообщает о каждом сохраненном файле.

## Проверки

```
python -m unittest -v
```

Проверяются языковые колонки, ошибочные таблицы, выборка, сохранность кэша при сетевых ошибках,
ограничение размера ответа, экспорты с разделителем в названии и неизменность входных данных.

## CI and coverage

```sh
python -m pip install -r requirements-dev.txt
python -m coverage run -m unittest discover -v
python -m coverage report
```

All tests run offline with temporary directories, fixed random sources and fake HTTP
responses. They cover parsing, input retries, sampling, cache validation, redirects,
download bounds, real DOCX round trips, atomic write failures and cleanup. CI uses
Python 3.12 and enforces 98% combined statement/branch coverage across the three
application modules. It uploads XML, HTML and text coverage reports.

CodeQL scans Python, and Dependabot checks pip dependencies and Actions weekly.
The proposed branch ruleset in `.github` requires both jobs and must be applied
separately through GitHub settings.
