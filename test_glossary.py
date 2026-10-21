import random
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from terms_loader import load_terms, MAX_DOWNLOAD
from terms_loader import Term, sample_terms
from terms_exporter import export_txt, export_docx

class GlossaryTests(unittest.TestCase):
    def test_sample_exact_unique(self):
        terms = [Term(str(i), "definition") for i in range(500)]
        self.assertEqual(len(sample_terms(terms + terms, 500, random.Random(1))), 500)
        with self.assertRaises(ValueError):
            sample_terms(terms, 501)

    def test_exports_preserve_input(self):
        terms = [Term("AC - DC", "definition")]
        with tempfile.TemporaryDirectory() as directory:
            export_docx(terms, "рус", directory)
            text = export_txt(terms, "рус", directory).read_text(encoding="utf-8")
            self.assertEqual(text, "AC - DC - definition\n")
            self.assertEqual(terms, [Term("AC - DC", "definition")])
            import docx
            document = docx.Document(Path(directory) / "glossary_ru.docx")
            self.assertEqual(document.tables[0].rows[1].cells[0].text, "AC - DC")

@unittest.skipUnless(importlib.util.find_spec('bs4'), 'BeautifulSoup dependency is not installed')
class ParserTests(unittest.TestCase):
    def test_language_pairs_and_delimiters(self):
        from terms_loader import parse_terms
        html='<table><tr><th>RU</th><th>KZ</th></tr><tr><td>AC - DC</td><td>Tok</td></tr><tr><td>definition</td><td>meaning</td></tr></table>'
        self.assertEqual(parse_terms(html,'рус'),[Term('AC - DC','definition')])
        self.assertEqual(parse_terms(html,'каз'),[Term('Tok','meaning')])
    def test_malformed_table_rejected(self):
        from terms_loader import parse_terms
        for html in ['<html>error</html>','<table><tr><th>header</th></tr><tr><td>unpaired</td></tr></table>',
                     '<table><tr><th>header</th></tr><tr><td>term</td></tr><tr><td></td></tr></table>']:
            with self.assertRaises(ValueError):parse_terms(html,'рус')


class FakeResponse:
    url = 'https://example.invalid/terms'
    history = []
    def __init__(self, chunks, error=None):
        self.chunks, self.error = chunks, error
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def raise_for_status(self):
        if self.error: raise self.error
    def iter_content(self, size): yield from self.chunks

class FakeSession:
    def __init__(self, response): self.response = response
    def get(self, url, **kwargs):
        assert kwargs['timeout'] == (5,20)
        return self.response

class DownloadTests(unittest.TestCase):
    def test_error_never_replaces_invalid_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)/'cache.html'
            cache.write_text('old invalid cache',encoding='utf-8')
            with patch('terms_loader.parse_terms',side_effect=ValueError('bad table')):
                with self.assertRaises(ValueError):
                    load_terms('рус',cache,FakeSession(FakeResponse([b'bad HTML'])))
            self.assertEqual(cache.read_text(), 'old invalid cache')
            self.assertEqual(len(list(Path(directory).iterdir())),1)
    def test_status_redirect_and_size_errors(self):
        responses=[FakeResponse([],ValueError('HTTP 500')),FakeResponse([b'x'*(MAX_DOWNLOAD+1)])]
        insecure=FakeResponse([]);insecure.url='http://example.invalid/terms';responses.append(insecure)
        with tempfile.TemporaryDirectory() as directory:
            cache=Path(directory)/'cache.html'
            for response in responses:
                with self.assertRaises(ValueError):load_terms('рус',cache,FakeSession(response))
                self.assertFalse(cache.exists())
    def test_validated_cache_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            cache=Path(directory)/'cache.html'
            with patch('terms_loader.parse_terms',return_value=[Term('name','definition')]):
                terms=load_terms('рус',cache,FakeSession(FakeResponse([b'validated HTML'])))
            self.assertEqual(terms,[Term('name','definition')])
            self.assertEqual(cache.read_text(),'validated HTML')


if __name__ == "__main__":
    unittest.main()
