import os
import tempfile

import pytest

from json_engine.api import JSONError, dump, dumps, load, loads


class TestLoadsFunction:
    """Testy funkcji loads()"""

    def test_loads_simple_object(self):
        result = loads('{"name": "Alice", "age": 30}')
        assert result == {"name": "Alice", "age": 30}

    def test_loads_simple_array(self):
        result = loads("[1, 2, 3, 4, 5]")
        assert result == [1, 2, 3, 4, 5]

    def test_loads_null(self):
        assert loads("null") is None

    def test_loads_boolean(self):
        assert loads("true") is True
        assert loads("false") is False

    def test_loads_number(self):
        assert loads("42") == 42
        assert loads("3.14") == 3.14

    def test_loads_string(self):
        assert loads('"hello world"') == "hello world"

    def test_loads_with_trace_disabled(self):
        result = loads('{"test": 123}', trace=False)
        assert result == {"test": 123}

    def test_loads_with_trace_enabled(self):
        result = loads('{"test": 123}', trace=True)
        assert result == {"test": 123}


class TestDumpsFunction:
    """Testy funkcji dumps()"""

    def test_dumps_simple_object(self):
        result = dumps({"name": "Alice", "age": 30})
        assert "Alice" in result
        assert "30" in result

    def test_dumps_simple_array(self):
        result = dumps([1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_dumps_null(self):
        assert dumps(None) == "null"

    def test_dumps_boolean(self):
        assert dumps(True) == "true"
        assert dumps(False) == "false"

    def test_dumps_number(self):
        assert dumps(42) == "42"
        assert dumps(3.14) == "3.14"

    def test_dumps_string(self):
        result = dumps("hello")
        assert result == '"hello"'


class TestLoadFunction:
    """Testy funkcji load() - czytanie z pliku"""

    def test_load_simple_object(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write('{"test": "value", "number": 42}')
            temp_path = f.name

        try:
            with open(temp_path, "r") as f:
                result = load(f)
            assert result == {"test": "value", "number": 42}
        finally:
            os.unlink(temp_path)

    def test_load_array(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write("[1, 2, 3, 4, 5]")
            temp_path = f.name

        try:
            with open(temp_path, "r") as f:
                result = load(f)
            assert result == [1, 2, 3, 4, 5]
        finally:
            os.unlink(temp_path)

    def test_load_with_trace(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write('{"trace": true}')
            temp_path = f.name

        try:
            with open(temp_path, "r") as f:
                result = load(f, trace=True)
            assert result == {"trace": True}
        finally:
            os.unlink(temp_path)

    def test_load_multiline_json(self):
        json_content = """{
            "name": "Test",
            "values": [1, 2, 3],
            "nested": {
                "key": "value"
            }
        }"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write(json_content)
            temp_path = f.name

        try:
            with open(temp_path, "r") as f:
                result = load(f)
            assert result["name"] == "Test"
            assert result["values"] == [1, 2, 3]
            assert result["nested"]["key"] == "value"
        finally:
            os.unlink(temp_path)


class TestDumpFunction:
    """Testy funkcji dump() - zapis do pliku"""

    def test_dump_simple_object(self):
        data = {"test": "value", "number": 42}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            with open(temp_path, "w") as f:
                dump(data, f)

            with open(temp_path, "r") as f:
                content = f.read()

            assert "test" in content
            assert "value" in content
            assert "42" in content
        finally:
            os.unlink(temp_path)

    def test_dump_array(self):
        data = [1, 2, 3, 4, 5]

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            with open(temp_path, "w") as f:
                dump(data, f)

            with open(temp_path, "r") as f:
                content = f.read()

            assert content == "[1, 2, 3, 4, 5]"
        finally:
            os.unlink(temp_path)

    def test_dump_complex_structure(self):
        data = {
            "users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}],
            "active": True,
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            with open(temp_path, "w") as f:
                dump(data, f)

            with open(temp_path, "r") as f:
                content = f.read()

            assert "Alice" in content
            assert "Bob" in content
            assert "true" in content
        finally:
            os.unlink(temp_path)


class TestRoundTrip:
    """Testy pełnego cyklu: dumps -> loads"""

    def test_roundtrip_object(self):
        original = {"name": "Test", "value": 123, "active": True}
        json_str = dumps(original)
        result = loads(json_str)
        assert result == original

    def test_roundtrip_array(self):
        original = [1, "two", 3.14, True, None]
        json_str = dumps(original)
        result = loads(json_str)
        assert result == original

    def test_roundtrip_nested_structure(self):
        original = {
            "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "metadata": {"count": 2, "active": True},
        }
        json_str = dumps(original)
        result = loads(json_str)
        assert result == original

    def test_roundtrip_with_escapes(self):
        original = {"text": 'He said "Hello"\nNew line'}
        json_str = dumps(original)
        result = loads(json_str)
        assert result == original


class TestRoundTripFile:
    """Testy pełnego cyklu: dump -> load"""

    def test_file_roundtrip_object(self):
        original = {"test": "data", "number": 42}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            # Zapisz
            with open(temp_path, "w") as f:
                dump(original, f)

            # Wczytaj
            with open(temp_path, "r") as f:
                result = load(f)

            assert result == original
        finally:
            os.unlink(temp_path)

    def test_file_roundtrip_complex(self):
        original = {
            "items": [1, 2, 3],
            "nested": {"key": "value"},
            "flags": [True, False, True],
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            with open(temp_path, "w") as f:
                dump(original, f)

            with open(temp_path, "r") as f:
                result = load(f)

            assert result == original
        finally:
            os.unlink(temp_path)


class TestJSONErrorExport:
    """Testy eksportu JSONError"""

    def test_json_error_is_available(self):
        # Sprawdź czy JSONError jest dostępny
        assert JSONError is not None

    def test_json_error_raised_on_invalid_json(self):
        with pytest.raises(JSONError):
            loads("invalid json")

    def test_json_error_raised_on_unterminated_string(self):
        with pytest.raises(JSONError):
            loads('"unterminated')

    def test_json_error_has_position_info(self):
        try:
            loads('{"key": @}')
        except JSONError as e:
            assert hasattr(e, "line")
            assert hasattr(e, "column")


class TestErrorHandling:
    """Testy obsługi błędów w API"""

    def test_loads_empty_string_error(self):
        with pytest.raises(ValueError):
            loads("")

    def test_loads_invalid_json(self):
        with pytest.raises(JSONError):
            loads("{invalid}")

    def test_dumps_non_serializable(self):
        class CustomClass:
            pass

        with pytest.raises(TypeError):
            dumps(CustomClass())

    def test_dumps_non_string_dict_keys(self):
        with pytest.raises(TypeError):
            dumps({123: "value"})


class TestEdgeCases:
    """Testy przypadków brzegowych API"""

    def test_loads_whitespace_only(self):
        with pytest.raises((ValueError, JSONError)):
            loads("   ")

    def test_dumps_empty_dict(self):
        assert dumps({}) == "{}"

    def test_dumps_empty_list(self):
        assert dumps([]) == "[]"

    def test_roundtrip_special_characters(self):
        original = {"text": 'Line1\nLine2\tTab"Quote'}
        json_str = dumps(original)
        result = loads(json_str)
        assert result["text"] == original["text"]

    def test_roundtrip_unicode(self):
        original = {"polish": "Zażółć gęślą jaźń"}
        json_str = dumps(original)
        result = loads(json_str)
        assert result == original

    def test_file_load_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            # Plik pusty
            temp_path = f.name

        try:
            with open(temp_path, "r") as f:
                with pytest.raises(ValueError):
                    load(f)
        finally:
            os.unlink(temp_path)


class TestAPIConsistency:
    """Testy spójności API"""

    def test_loads_dumps_inverse_operations(self):
        # dumps(loads(x)) powinno być blisko x (z uwzględnieniem formatowania)
        original_json = '{"a":1,"b":2}'
        parsed = loads(original_json)
        re_encoded = dumps(parsed)
        re_parsed = loads(re_encoded)
        assert parsed == re_parsed

    def test_multiple_loads_same_result(self):
        json_str = '{"test": [1, 2, 3]}'
        result1 = loads(json_str)
        result2 = loads(json_str)
        assert result1 == result2

    def test_multiple_dumps_same_result(self):
        data = {"test": [1, 2, 3]}
        result1 = dumps(data)
        result2 = dumps(data)
        assert result1 == result2
