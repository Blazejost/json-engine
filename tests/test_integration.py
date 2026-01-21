import os
import tempfile

import pytest

from json_engine.api import dump, dumps, load, loads
from json_engine.tokenizer import tokenize


class TestEndToEndWorkflow:
    """Testy pełnego przepływu pracy z JSON"""

    def test_complete_workflow_object(self):
        # 1. Stwórz dane Python
        python_data = {
            "user": {"name": "Alice", "age": 30, "email": "alice@example.com"},
            "settings": {"notifications": True, "theme": "dark"},
        }

        # 2. Serializuj do JSON
        json_string = dumps(python_data)
        assert isinstance(json_string, str)
        assert "Alice" in json_string

        # 3. Deserializuj z powrotem
        parsed_data = loads(json_string)
        assert parsed_data == python_data

        # 4. Zapisz do pliku
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            with open(temp_path, "w") as f:
                dump(parsed_data, f)

            # 5. Wczytaj z pliku
            with open(temp_path, "r") as f:
                loaded_data = load(f)

            # 6. Sprawdź zgodność
            assert loaded_data == python_data
        finally:
            os.unlink(temp_path)

    def test_complete_workflow_array(self):
        python_data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
        ]

        json_string = dumps(python_data)
        parsed_data = loads(json_string)
        assert parsed_data == python_data


class TestRealWorldJSONStructures:
    """Testy z realistycznymi strukturami JSON"""

    def test_user_profile_structure(self):
        profile = {
            "userId": "12345",
            "username": "alice_dev",
            "email": "alice@example.com",
            "profile": {
                "firstName": "Alice",
                "lastName": "Johnson",
                "age": 28,
                "avatar": "https://example.com/avatar.jpg",
            },
            "preferences": {
                "language": "en",
                "timezone": "UTC",
                "notifications": {"email": True, "push": False, "sms": False},
            },
            "roles": ["user", "developer", "admin"],
            "createdAt": "2024-01-15T10:30:00Z",
            "isActive": True,
        }

        json_str = dumps(profile)
        parsed = loads(json_str)

        assert parsed["userId"] == "12345"
        assert parsed["preferences"]["notifications"]["email"] is True
        assert "developer" in parsed["roles"]
        assert parsed["isActive"] is True

    def test_api_response_structure(self):
        api_response = {
            "status": "success",
            "code": 200,
            "data": {
                "items": [
                    {"id": 1, "title": "First", "completed": True},
                    {"id": 2, "title": "Second", "completed": False},
                ],
                "pagination": {"page": 1, "perPage": 10, "total": 2, "hasMore": False},
            },
            "meta": {"timestamp": "2024-01-15T12:00:00Z", "requestId": "abc-123-def"},
        }

        json_str = dumps(api_response)
        parsed = loads(json_str)

        assert parsed["status"] == "success"
        assert len(parsed["data"]["items"]) == 2
        assert parsed["data"]["pagination"]["hasMore"] is False

    def test_configuration_file_structure(self):
        config = {
            "app": {"name": "MyApp", "version": "1.0.0", "environment": "production"},
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "mydb",
                "ssl": True,
            },
            "cache": {
                "enabled": True,
                "ttl": 3600,
                "providers": ["redis", "memcached"],
            },
            "features": {
                "enableBeta": False,
                "maxUploadSize": 10485760,
                "allowedFormats": ["jpg", "png", "pdf"],
            },
        }

        json_str = dumps(config)
        parsed = loads(json_str)

        assert parsed["app"]["version"] == "1.0.0"
        assert parsed["database"]["port"] == 5432
        assert "redis" in parsed["cache"]["providers"]
        assert parsed["features"]["enableBeta"] is False


class TestComplexDataStructures:
    """Testy złożonych struktur danych"""

    def test_deeply_nested_structure(self):
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {"level5": {"value": "deep", "items": [1, 2, 3]}}
                    }
                }
            }
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        assert (
            parsed["level1"]["level2"]["level3"]["level4"]["level5"]["value"] == "deep"
        )
        assert parsed["level1"]["level2"]["level3"]["level4"]["level5"]["items"] == [
            1,
            2,
            3,
        ]

    def test_mixed_array_structures(self):
        data = {
            "mixed": [1, "string", True, None, {"nested": "object"}, [1, 2, 3], 3.14]
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        assert parsed["mixed"][0] == 1
        assert parsed["mixed"][1] == "string"
        assert parsed["mixed"][2] is True
        assert parsed["mixed"][3] is None
        assert parsed["mixed"][4]["nested"] == "object"
        assert parsed["mixed"][5] == [1, 2, 3]
        assert parsed["mixed"][6] == 3.14

    def test_array_of_complex_objects(self):
        data = [
            {
                "id": 1,
                "tags": ["python", "json"],
                "metadata": {"views": 100, "likes": 50},
            },
            {
                "id": 2,
                "tags": ["javascript", "api"],
                "metadata": {"views": 200, "likes": 75},
            },
        ]

        json_str = dumps(data)
        parsed = loads(json_str)

        assert len(parsed) == 2
        assert parsed[0]["tags"][0] == "python"
        assert parsed[1]["metadata"]["views"] == 200


class TestEdgeCasesIntegration:
    """Testy przypadków brzegowych w integracjach"""

    def test_empty_structures(self):
        data = {
            "emptyObject": {},
            "emptyArray": [],
            "arrayWithEmpty": [{}, [], ""],
            "emptyString": "",
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        assert parsed["emptyObject"] == {}
        assert parsed["emptyArray"] == []
        assert parsed["arrayWithEmpty"] == [{}, [], ""]
        assert parsed["emptyString"] == ""

    def test_special_characters_in_strings(self):
        data = {
            "quotes": 'He said "Hello"',
            "newlines": "Line 1\nLine 2\nLine 3",
            "tabs": "Col1\tCol2\tCol3",
            "backslash": "Path\\to\\file",
            "mixed": 'Text with "quotes" and\nnewlines\tand\\backslashes',
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        assert parsed["quotes"] == 'He said "Hello"'
        assert parsed["newlines"] == "Line 1\nLine 2\nLine 3"
        assert parsed["tabs"] == "Col1\tCol2\tCol3"
        assert parsed["backslash"] == "Path\\to\\file"
        assert parsed["mixed"] == 'Text with "quotes" and\nnewlines\tand\\backslashes'

    def test_numeric_edge_cases(self):
        data = {
            "zero": 0,
            "negativeZero": -0,
            "largeInt": 999999999999999,
            "smallFloat": 0.0000001,
            "largeFloat": 1e100,
            "negative": -42.5,
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        assert parsed["zero"] == 0
        assert parsed["largeInt"] == 999999999999999
        assert isinstance(parsed["smallFloat"], float)

    def test_boolean_vs_numeric_values(self):
        data = {
            "trueValue": True,
            "falseValue": False,
            "zero": 0,
            "one": 1,
            "array": [True, False, 0, 1],
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        # Sprawdź że boolean nie zamienił się na int
        assert parsed["trueValue"] is True
        assert parsed["falseValue"] is False
        assert parsed["zero"] == 0
        assert parsed["one"] == 1


class TestFileOperationsIntegration:
    """Testy integracyjne operacji plikowych"""

    def test_save_and_load_multiple_times(self):
        original = {"data": [1, 2, 3], "flag": True}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            # Pierwsze zapisanie
            with open(temp_path, "w") as f:
                dump(original, f)

            # Pierwsze wczytanie
            with open(temp_path, "r") as f:
                first_load = load(f)

            # Drugie zapisanie
            with open(temp_path, "w") as f:
                dump(first_load, f)

            # Drugie wczytanie
            with open(temp_path, "r") as f:
                second_load = load(f)

            assert original == first_load == second_load
        finally:
            os.unlink(temp_path)

    def test_multiple_objects_in_separate_files(self):
        objects = [
            {"id": 1, "name": "First"},
            {"id": 2, "name": "Second"},
            {"id": 3, "name": "Third"},
        ]

        temp_files = []

        try:
            # Zapisz każdy obiekt do osobnego pliku
            for obj in objects:
                with tempfile.NamedTemporaryFile(
                    mode="w", delete=False, suffix=".json"
                ) as f:
                    temp_files.append(f.name)
                    dump(obj, f)

            # Wczytaj wszystkie pliki
            loaded_objects = []
            for temp_file in temp_files:
                with open(temp_file, "r") as f:
                    loaded_objects.append(load(f))

            assert loaded_objects == objects
        finally:
            for temp_file in temp_files:
                os.unlink(temp_file)


class TestTokenizerIntegration:
    """Testy integracji tokenizera z całym systemem"""

    def test_tokenizer_with_parser_integration(self):
        json_str = '{"key": "value", "number": 123}'

        # Sprawdź że tokenizacja działa
        tokens = list(tokenize(json_str))
        assert len(tokens) > 0

        # Sprawdź że parser może przetworzyć te tokeny
        parsed = loads(json_str)
        assert parsed == {"key": "value", "number": 123}

    def test_tokenizer_errors_propagate(self):
        # Błąd tokenizacji powinien być wyłapany przez loads
        with pytest.raises(Exception):  # TokenizeError lub JSONError
            loads('{"invalid": @}')


class TestPerformanceIntegration:
    """Testy wydajnościowe (podstawowe)"""

    def test_large_array_performance(self):
        # Duża tablica - sprawdzamy czy działa, nie mierzymy czasu
        large_array = list(range(1000))
        json_str = dumps(large_array)
        parsed = loads(json_str)
        assert len(parsed) == 1000
        assert parsed[0] == 0
        assert parsed[-1] == 999

    def test_large_object_performance(self):
        # Duży obiekt
        large_object = {f"key_{i}": i for i in range(500)}
        json_str = dumps(large_object)
        parsed = loads(json_str)
        assert len(parsed) == 500
        assert parsed["key_250"] == 250

    def test_deep_nesting_performance(self):
        # Głęboko zagnieżdżona struktura
        depth = 50
        data = {"value": "deep"}
        for i in range(depth):
            data = {"nested": data}

        json_str = dumps(data)
        parsed = loads(json_str)

        # Sprawdź głębokość
        current = parsed
        for i in range(depth):
            assert "nested" in current
            current = current["nested"]
        assert current["value"] == "deep"


class TestCompatibilityWithStandardJSON:
    """Testy zgodności ze standardem JSON"""

    def test_standard_json_types(self):
        # Wszystkie standardowe typy JSON
        data = {
            "string": "text",
            "number_int": 42,
            "number_float": 3.14,
            "boolean_true": True,
            "boolean_false": False,
            "null": None,
            "array": [1, 2, 3],
            "object": {"nested": "value"},
        }

        json_str = dumps(data)
        parsed = loads(json_str)

        assert isinstance(parsed["string"], str)
        assert isinstance(parsed["number_int"], int)
        assert isinstance(parsed["number_float"], float)
        assert isinstance(parsed["boolean_true"], bool)
        assert isinstance(parsed["boolean_false"], bool)
        assert parsed["null"] is None
        assert isinstance(parsed["array"], list)
        assert isinstance(parsed["object"], dict)
