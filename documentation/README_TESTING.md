# JSON Engine - Testing Guide

## 📋 Przegląd Testów

Projekt zawiera kompleksowy zestaw testów automatycznych pokrywających wszystkie komponenty JSON engine.

### Struktura Testów

```
tests/
├── test_tokenizer.py      # Testy tokenizera (69+ testów)
├── test_parser.py          # Testy parsera (52+ testów)
├── test_encoder.py         # Testy enkodera (48+ testów)
├── test_api.py             # Testy API (45+ testów)
├── test_integration.py     # Testy integracyjne (40+ testów)
└── conftest.py             # Fixtures i konfiguracja
```

**Łącznie: 250+ testów automatycznych**

## 🚀 Uruchamianie Testów

### Wymagania

Instalacja zależności deweloperskich przy użyciu `uv`:

```bash
# Zainstaluj uv (jeśli nie masz)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Synchronizuj projekt i zależności deweloperskie
uv sync --all-extras
```

### Podstawowe Uruchomienie

```bash
# Wszystkie testy
uv run pytest

# Testy z verbose output
uv run pytest -v

# Testy z coverage
uv run pytest --cov=json_engine --cov-report=html

# Konkretny plik testowy
uv run pytest tests/test_tokenizer.py

# Konkretna klasa testowa
uv run pytest tests/test_parser.py::TestBasicParsing

# Konkretny test
uv run pytest tests/test_api.py::TestLoadsFunction::test_loads_simple_object
```

### Filtorwanie Testów

```bash
# Tylko testy jednostkowe
uv run pytest -m unit

# Tylko testy integracyjne
uv run pytest -m integration

# Wszystko oprócz wolnych testów
uv run pytest -m "not slow"

# Testy zawierające słowo "error" w nazwie
uv run pytest -k "error"
```

## 📊 Pokrycie Kodu (Coverage)

### Generowanie Raportu

```bash
# Raport w terminalu
uv run pytest --cov=json_engine --cov-report=term-missing

# Raport HTML (szczegółowy)
uv run pytest --cov=json_engine --cov-report=html

# Otwórz raport HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Oczekiwane Pokrycie

- **tokenizer.py**: > 95%
- **parser.py**: > 90%
- **encoder.py**: > 95%
- **api.py**: > 95%

## 🧪 Kategorie Testów

### 1. Testy Tokenizera (`test_tokenizer.py`)

- **TestTokenizerBasics**: Podstawowe tokeny JSON
- **TestStringTokens**: Tokenizacja stringów i escape sequences
- **TestNumberTokens**: Wszystkie formaty liczb
- **TestKeywordTokens**: true, false, null
- **TestLineAndColumnTracking**: Śledzenie pozycji błędów
- **TestComplexStructures**: Zagnieżdżone struktury
- **TestErrorHandling**: Obsługa błędów tokenizacji

### 2. Testy Parsera (`test_parser.py`)

- **TestBasicParsing**: Parsowanie podstawowych typów
- **TestObjectParsing**: Obiekty JSON
- **TestArrayParsing**: Tablice JSON
- **TestComplexStructures**: Złożone zagnieżdżenia
- **TestErrorHandling**: Błędy składniowe
- **TestWhitespaceHandling**: Whitespace
- **TestEscapeSequences**: Znaki specjalne
- **TestNumberParsing**: Typy liczb

### 3. Testy Enkodera (`test_encoder.py`)

- **TestBasicEncoding**: Podstawowe typy
- **TestStringEncoding**: Escape'owanie stringów
- **TestArrayEncoding**: Tablice
- **TestObjectEncoding**: Obiekty
- **TestComplexStructures**: Złożone struktury
- **TestErrorHandling**: Nieserializowalne obiekty
- **TestBooleanHandling**: Boolean vs int

### 4. Testy API (`test_api.py`)

- **TestLoadsFunction**: Deserializacja
- **TestDumpsFunction**: Serializacja
- **TestLoadFunction**: Czytanie z pliku
- **TestDumpFunction**: Zapis do pliku
- **TestRoundTrip**: Pełny cykl encode/decode
- **TestJSONErrorExport**: Eksport błędów

### 5. Testy Integracyjne (`test_integration.py`)

- **TestEndToEndWorkflow**: Kompletne przepływy pracy
- **TestRealWorldJSONStructures**: Realistyczne dane
- **TestComplexDataStructures**: Bardzo złożone struktury
- **TestEdgeCasesIntegration**: Przypadki brzegowe
- **TestFileOperationsIntegration**: Operacje plikowe
- **TestCompatibilityWithStandardJSON**: Zgodność ze standardem

## 🎯 Wzorce Projektowe w Testach

### 1. **Arrange-Act-Assert (AAA)**

Wszystkie testy używają wzorca AAA:

```python
def test_example(self):
    # Arrange - przygotowanie danych
    data = {"key": "value"}
    
    # Act - wykonanie akcji
    result = dumps(data)
    
    # Assert - sprawdzenie wyniku
    assert "key" in result
```

### 2. **Fixtures (DRY Principle)**

Używamy fixtures do wspólnych danych:

```python
@pytest.fixture
def sample_json_object():
    return {"name": "Test", "age": 30}

def test_with_fixture(sample_json_object):
    result = dumps(sample_json_object)
    assert "Test" in result
```

### 3. **Parametryzacja**

Dla wielu podobnych przypadków:

```python
@pytest.mark.parametrize("input,expected", [
    ("true", True),
    ("false", False),
    ("null", None),
])
def test_keywords(input, expected):
    assert loads(input) == expected
```

## 📈 Dane Testowe

### Przypadki Testowe

1. **Happy Path**: Poprawne dane JSON
2. **Edge Cases**: Puste struktury, głębokie zagnieżdżenia
3. **Error Cases**: Błędna składnia, nieprawidłowe dane
4. **Performance**: Duże struktury (1000+ elementów)
5. **Real World**: Realistyczne struktury API

### Pokrycie Błędów

- ✅ Niezamknięte stringi
- ✅ Nieprawidłowe escape sequences
- ✅ Błędne liczby
- ✅ Brakujące przecinki
- ✅ Dodatkowe dane po JSON
- ✅ Nieserializowalne obiekty

## 🔧 Continuous Integration

### GitHub Actions (przykład)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Run tests
        run: uv run pytest --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 📝 Dokumentacja Testów

### Struktura Danych - Co Testujemy

1. **Lista tokenów** (`List[Token]`) - w parserze
2. **Dictionary** - dla obiektów JSON
3. **Lista** - dla tablic JSON
4. **Typy prymitywne** - int, float, str, bool, None

### Algorytmy - Co Testujemy

1. **Tokenizacja** - Regex dla liczb, pętle dla stringów
2. **Parsowanie** - Recursive descent parser
3. **Encodowanie** - Rekurencyjne przetwarzanie struktur

## 🎓 Dla Zaliczenia

### Wymagania Spełnione ✅

1. **Wzorce architektoniczne**:
   - Strategy Pattern (parse_value, parse_object, parse_array)
   - Single Responsibility Principle
   - Separation of Concerns

2. **Struktury danych**:
   - Lista tokenów dla parsera
   - Dictionary/List dla JSON
   - Dokumentacja w komentarzach

3. **Testy systematyczne**:
   - 250+ testów automatycznych
   - Coverage > 90%
   - Unit + Integration tests

4. **Przypadki testowe**:
   - Happy path scenarios
   - Edge cases
   - Error handling
   - Complex structures

### Uruchomienie przed prezentacją

```bash
# 1. Pełne testy z coverage
uv run pytest --cov=json_engine --cov-report=html --cov-report=term

# 2. Sprawdź coverage report
open htmlcov/index.html

# 3. Uruchom konkretne kategorie dla demo
uv run pytest tests/test_tokenizer.py -v
uv run pytest tests/test_integration.py -v

# 4. Sprawdź czy wszystko przechodzi
uv run pytest --tb=short
```

## 🐛 Debugging Testów

```bash
# Zatrzymaj się przy pierwszym błędzie
uv run pytest -x

# Więcej informacji o błędzie
uv run pytest --tb=long

# Uruchom konkretny test z print statements
uv run pytest tests/test_parser.py::TestBasicParsing::test_parse_null -s

# PDB debugger przy błędzie
uv run pytest --pdb
```

## 📚 Dodatkowe Zasoby

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [JSON Specification](https://www.json.org/)