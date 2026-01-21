import pytest

from json_engine.encoder import JSONEncoder


class TestBasicEncoding:
    """Testy podstawowego encodowania wartości"""

    def test_encode_none(self):
        encoder = JSONEncoder()
        assert encoder.encode(None) == "null"

    def test_encode_true(self):
        encoder = JSONEncoder()
        assert encoder.encode(True) == "true"

    def test_encode_false(self):
        encoder = JSONEncoder()
        assert encoder.encode(False) == "false"

    def test_encode_integer(self):
        encoder = JSONEncoder()
        assert encoder.encode(42) == "42"
        assert encoder.encode(-17) == "-17"
        assert encoder.encode(0) == "0"

    def test_encode_float(self):
        encoder = JSONEncoder()
        assert encoder.encode(3.14) == "3.14"
        assert encoder.encode(-2.5) == "-2.5"
        assert encoder.encode(1e10) == "10000000000.0"


class TestStringEncoding:
    """Testy encodowania stringów"""

    def test_encode_simple_string(self):
        encoder = JSONEncoder()
        assert encoder.encode("hello") == '"hello"'

    def test_encode_empty_string(self):
        encoder = JSONEncoder()
        assert encoder.encode("") == '""'

    def test_encode_string_with_spaces(self):
        encoder = JSONEncoder()
        assert encoder.encode("hello world") == '"hello world"'

    def test_encode_string_with_quotes(self):
        encoder = JSONEncoder()
        result = encoder.encode('He said "Hello"')
        assert result == r'"He said \"Hello\""'

    def test_encode_string_with_backslash(self):
        encoder = JSONEncoder()
        result = encoder.encode(r"C:\Users\test")
        assert result == r'"C:\\Users\\test"'

    def test_encode_string_with_newline(self):
        encoder = JSONEncoder()
        result = encoder.encode("line1\nline2")
        assert result == r'"line1\nline2"'

    def test_encode_combined_escapes(self):
        encoder = JSONEncoder()
        result = encoder.encode('text\n"quoted"\ttab\\backslash')
        assert "\\n" in result
        assert '\\"' in result
        assert "\\\\" in result


class TestArrayEncoding:
    """Testy encodowania tablic"""

    def test_encode_empty_array(self):
        encoder = JSONEncoder()
        assert encoder.encode([]) == "[]"

    def test_encode_simple_array(self):
        encoder = JSONEncoder()
        result = encoder.encode([1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_encode_array_with_various_types(self):
        encoder = JSONEncoder()
        result = encoder.encode([1, "text", True, None])
        assert "1" in result
        assert '"text"' in result
        assert "true" in result
        assert "null" in result

    def test_encode_nested_array(self):
        encoder = JSONEncoder()
        result = encoder.encode([[1, 2], [3, 4]])
        assert result == "[[1, 2], [3, 4]]"

    def test_encode_deeply_nested_array(self):
        encoder = JSONEncoder()
        result = encoder.encode([[[1]]])
        assert result == "[[[1]]]"


class TestObjectEncoding:
    """Testy encodowania obiektów"""

    def test_encode_empty_object(self):
        encoder = JSONEncoder()
        assert encoder.encode({}) == "{}"

    def test_encode_simple_object(self):
        encoder = JSONEncoder()
        result = encoder.encode({"name": "John", "age": 30})
        # Kolejność kluczy może się różnić
        assert '"name": "John"' in result or '"name":"John"' in result
        assert '"age": 30' in result or '"age":30' in result
        assert result.startswith("{")
        assert result.endswith("}")

    def test_encode_object_with_various_types(self):
        encoder = JSONEncoder()
        result = encoder.encode(
            {"string": "text", "number": 42, "boolean": True, "null": None}
        )
        assert '"string": "text"' in result
        assert '"number": 42' in result
        assert '"boolean": true' in result
        assert '"null": null' in result

    def test_encode_nested_object(self):
        encoder = JSONEncoder()
        result = encoder.encode({"outer": {"inner": "value"}})
        assert "outer" in result
        assert "inner" in result
        assert "value" in result

    def test_encode_object_with_array_value(self):
        encoder = JSONEncoder()
        result = encoder.encode({"numbers": [1, 2, 3]})
        assert '"numbers": [1, 2, 3]' in result or '"numbers":[1, 2, 3]' in result


class TestComplexStructures:
    """Testy encodowania złożonych struktur"""

    def test_encode_complex_nested_structure(self):
        encoder = JSONEncoder()
        data = {
            "users": [
                {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]},
                {"name": "Bob", "age": 25, "hobbies": ["gaming"]},
            ],
            "count": 2,
        }
        result = encoder.encode(data)
        assert "users" in result
        assert "Alice" in result
        assert "Bob" in result
        assert "reading" in result
        assert "coding" in result
        assert "gaming" in result
        assert '"count": 2' in result or '"count":2' in result

    def test_encode_mixed_nesting(self):
        encoder = JSONEncoder()
        data = {"a": [{"b": [1, 2, {"c": 3}]}]}
        result = encoder.encode(data)
        assert '"a"' in result
        assert '"b"' in result
        assert '"c": 3' in result or '"c":3' in result


class TestErrorHandling:
    """Testy obsługi błędów"""

    def test_encode_non_string_key_raises_error(self):
        encoder = JSONEncoder()
        with pytest.raises(TypeError, match="Keys must be strings"):
            encoder.encode({123: "value"})

    def test_encode_non_serializable_object_raises_error(self):
        encoder = JSONEncoder()

        class CustomClass:
            pass

        obj = CustomClass()
        with pytest.raises(TypeError, match="not JSON serializable"):
            encoder.encode(obj)

    def test_encode_set_raises_error(self):
        encoder = JSONEncoder()
        with pytest.raises(TypeError):
            encoder.encode({1, 2, 3})

    def test_encode_tuple_raises_error(self):
        encoder = JSONEncoder()
        # Tuple nie jest obsługiwany przez obecny encoder
        with pytest.raises(TypeError):
            encoder.encode((1, 2, 3))


class TestBooleanHandling:
    """Testy specjalnej obsługi boolean (musi być przed int)"""

    def test_true_not_encoded_as_one(self):
        encoder = JSONEncoder()
        result = encoder.encode(True)
        assert result == "true"
        assert result != "1"

    def test_false_not_encoded_as_zero(self):
        encoder = JSONEncoder()
        result = encoder.encode(False)
        assert result == "false"
        assert result != "0"

    def test_boolean_in_array(self):
        encoder = JSONEncoder()
        result = encoder.encode([True, False, 1, 0])
        assert "true" in result
        assert "false" in result
        # Sprawdź że są w odpowiedniej kolejności
        assert result.index("true") < result.index("false")


class TestEdgeCases:
    """Testy przypadków brzegowych"""

    def test_encode_very_long_string(self):
        encoder = JSONEncoder()
        long_str = "a" * 10000
        result = encoder.encode(long_str)
        assert len(result) >= 10000
        assert result.startswith('"')
        assert result.endswith('"')

    def test_encode_large_number(self):
        encoder = JSONEncoder()
        result = encoder.encode(999999999999999)
        assert result == "999999999999999"

    def test_encode_very_small_number(self):
        encoder = JSONEncoder()
        result = encoder.encode(0.0000001)
        assert "e-" in result.lower() or "0.0000001" in result

    def test_encode_deeply_nested_structure(self):
        encoder = JSONEncoder()
        # 10 poziomów zagnieżdżenia
        data = {
            "a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"i": {"j": "value"}}}}}}}}}
        }
        result = encoder.encode(data)
        assert result.count("{") == 10
        assert result.count("}") == 10

    def test_encode_empty_nested_structures(self):
        encoder = JSONEncoder()
        result = encoder.encode({"empty_obj": {}, "empty_arr": []})
        assert "{}" in result
        assert "[]" in result

    def test_encode_object_with_many_keys(self):
        encoder = JSONEncoder()
        data = {f"key{i}": i for i in range(100)}
        result = encoder.encode(data)
        assert result.count(":") == 100

    def test_encode_unicode_string(self):
        encoder = JSONEncoder()
        result = encoder.encode("Zażółć gęślą jaźń")
        assert "Zażółć" in result
        assert "gęślą" in result
        assert "jaźń" in result

    def test_encode_special_characters(self):
        encoder = JSONEncoder()
        result = encoder.encode("!@#$%^&*()_+-=[]{}|;:',.<>?")
        # Tylko \, ", i \n powinny być escaped
        assert "\\" in result  # backslash escaped
        assert '"' in result  # quote jest w wynikowym stringu


class TestConsistency:
    """Testy spójności encodowania"""

    def test_encode_preserves_order_in_array(self):
        encoder = JSONEncoder()
        result = encoder.encode([1, 2, 3, 4, 5])
        # Sprawdź że liczby są w odpowiedniej kolejności
        indices = [result.index(str(i)) for i in range(1, 6)]
        assert indices == sorted(indices)

    def test_encode_null_vs_empty_string(self):
        encoder = JSONEncoder()
        null_result = encoder.encode(None)
        empty_result = encoder.encode("")
        assert null_result == "null"
        assert empty_result == '""'
        assert null_result != empty_result

    def test_encode_zero_vs_false(self):
        encoder = JSONEncoder()
        zero_result = encoder.encode(0)
        false_result = encoder.encode(False)
        assert zero_result == "0"
        assert false_result == "false"
        assert zero_result != false_result
