"""
Pytest configuration and shared fixtures
"""

import pytest

from json_engine.api import dumps


@pytest.fixture
def sample_json_object():
    """Fixture: Przykładowy obiekt JSON"""
    return {"name": "Test User", "age": 30, "active": True, "email": "test@example.com"}


@pytest.fixture
def sample_json_array():
    """Fixture: Przykładowa tablica JSON"""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def complex_json_structure():
    """Fixture: Złożona struktura JSON"""
    return {
        "users": [
            {
                "id": 1,
                "name": "Alice",
                "roles": ["admin", "user"],
                "settings": {"theme": "dark", "notifications": True},
            },
            {
                "id": 2,
                "name": "Bob",
                "roles": ["user"],
                "settings": {"theme": "light", "notifications": False},
            },
        ],
        "metadata": {"version": "1.0", "created": "2024-01-15", "count": 2},
    }


@pytest.fixture
def temp_json_file(tmp_path):
    """Fixture: Tymczasowy plik JSON"""

    def _create_temp_file(data):
        file_path = tmp_path / "test.json"
        with open(file_path, "w") as f:
            f.write(dumps(data))
        return file_path

    return _create_temp_file


@pytest.fixture
def json_with_special_chars():
    """Fixture: JSON ze znakami specjalnymi"""
    return {
        "quotes": 'Text with "quotes"',
        "newlines": "Line 1\nLine 2",
        "tabs": "Col1\tCol2",
        "backslash": "Path\\to\\file",
        "unicode": "Zażółć gęślą jaźń",
    }


@pytest.fixture
def empty_structures():
    """Fixture: Puste struktury JSON"""
    return {"empty_object": {}, "empty_array": [], "empty_string": ""}


@pytest.fixture
def numeric_edge_cases():
    """Fixture: Przypadki brzegowe dla liczb"""
    return {
        "zero": 0,
        "negative": -42,
        "float": 3.14,
        "scientific": 1e10,
        "large": 999999999999999,
    }


# Konfiguracja markers
def pytest_configure(config):
    """Rejestracja custom markers"""
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")


# Hook do raportowania
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook do dodawania informacji o testach"""
    outcome = yield
    rep = outcome.get_result()

    # Dodaj informacje o module do raportu
    if rep.when == "call":
        rep.module_name = item.module.__name__ if hasattr(item, "module") else "unknown"
