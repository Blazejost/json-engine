import pytest

from json_engine.parser import JSONDecoder
from json_engine.tokenizer import TokenizeError


class TestBasicParsing:
    """Testy podstawowego parsowania wartości"""

    def test_parse_null(self):
        decoder = JSONDecoder()
        assert decoder.decode("null") is None

    def test_parse_true(self):
        decoder = JSONDecoder()
        assert decoder.decode("true") is True

    def test_parse_false(self):
        decoder = JSONDecoder()
        assert decoder.decode("false") is False

    def test_parse_integer(self):
        decoder = JSONDecoder()
        assert decoder.decode("42") == 42
        assert decoder.decode("-17") == -17
        assert decoder.decode("0") == 0

    def test_parse_float(self):
        decoder = JSONDecoder()
        assert decoder.decode("3.14") == 3.14
        assert decoder.decode("-2.5") == -2.5
        assert decoder.decode("1e10") == 1e10
        assert decoder.decode("1.5e-5") == 1.5e-5

    def test_parse_string(self):
        decoder = JSONDecoder()
        assert decoder.decode('"hello"') == "hello"
        assert decoder.decode('""') == ""
        assert decoder.decode('"hello world"') == "hello world"


class TestObjectParsing:
    """Testy parsowania obiektów JSON"""

    def test_empty_object(self):
        decoder = JSONDecoder()
        result = decoder.decode("{}")
        assert result == {}
        assert isinstance(result, dict)

    def test_simple_object(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"name": "John", "age": 30}')
        assert result == {"name": "John", "age": 30}

    def test_object_with_various_types(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"str": "text", "num": 42, "bool": true, "nil": null}')
        assert result == {"str": "text", "num": 42, "bool": True, "nil": None}

    def test_nested_object(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"outer": {"inner": {"deep": "value"}}}')
        assert result == {"outer": {"inner": {"deep": "value"}}}

    def test_object_with_array_value(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"numbers": [1, 2, 3]}')
        assert result == {"numbers": [1, 2, 3]}


class TestArrayParsing:
    """Testy parsowania tablic JSON"""

    def test_empty_array(self):
        decoder = JSONDecoder()
        result = decoder.decode("[]")
        assert result == []
        assert isinstance(result, list)

    def test_simple_array(self):
        decoder = JSONDecoder()
        result = decoder.decode("[1, 2, 3, 4, 5]")
        assert result == [1, 2, 3, 4, 5]

    def test_array_with_various_types(self):
        decoder = JSONDecoder()
        result = decoder.decode('[1, "two", true, null, 3.14]')
        assert result == [1, "two", True, None, 3.14]

    def test_nested_array(self):
        decoder = JSONDecoder()
        result = decoder.decode("[[1, 2], [3, 4], [5, 6]]")
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_array_of_objects(self):
        decoder = JSONDecoder()
        result = decoder.decode('[{"id": 1}, {"id": 2}, {"id": 3}]')
        assert result == [{"id": 1}, {"id": 2}, {"id": 3}]


class TestComplexStructures:
    """Testy złożonych struktur JSON"""

    def test_deeply_nested_structure(self):
        decoder = JSONDecoder()
        json_str = """
        {
            "users": [
                {
                    "name": "Alice",
                    "age": 30,
                    "address": {
                        "city": "Warsaw",
                        "country": "Poland"
                    },
                    "hobbies": ["reading", "coding"]
                },
                {
                    "name": "Bob",
                    "age": 25,
                    "address": {
                        "city": "Krakow",
                        "country": "Poland"
                    },
                    "hobbies": ["gaming", "music"]
                }
            ],
            "count": 2
        }
        """
        result = decoder.decode(json_str)
        assert result["count"] == 2
        assert len(result["users"]) == 2
        assert result["users"][0]["name"] == "Alice"
        assert result["users"][0]["address"]["city"] == "Warsaw"
        assert result["users"][1]["hobbies"][0] == "gaming"

    def test_mixed_nesting(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"a": [{"b": [1, 2, {"c": 3}]}]}')
        assert result["a"][0]["b"][2]["c"] == 3

    def test_array_with_nested_objects_and_arrays(self):
        decoder = JSONDecoder()
        json_str = '[{"items": [1, 2, 3]}, {"items": [4, 5, 6]}]'
        result = decoder.decode(json_str)
        assert result[0]["items"] == [1, 2, 3]
        assert result[1]["items"] == [4, 5, 6]


class TestErrorHandling:
    """Testy obsługi błędów parsowania"""

    def test_empty_string_error(self):
        decoder = JSONDecoder()
        with pytest.raises(ValueError, match="Empty string"):
            decoder.decode("")

    def test_none_input_error(self):
        decoder = JSONDecoder()
        with pytest.raises(ValueError, match="Empty string"):
            decoder.decode(None)

    def test_unexpected_token_error(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError, match="Unexpected token"):
            decoder.decode("{:}")

    def test_missing_colon_in_object(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError, match="Expected ':'"):
            decoder.decode('{"key" "value"}')

    def test_missing_value_in_object(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError, match="Expected string as object key"):
            decoder.decode('{123: "value"}')

    def test_trailing_comma_in_object(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError):
            decoder.decode('{"a": 1,}')

    def test_trailing_comma_in_array(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError):
            decoder.decode("[1, 2, 3,]")

    def test_missing_comma_in_object(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError, match="Expected ',' or '}'"):
            decoder.decode('{"a": 1 "b": 2}')

    def test_missing_comma_in_array(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError, match="Expected ',' or ']'"):
            decoder.decode("[1 2 3]")

    def test_extra_data_after_json(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError, match="Extra data"):
            decoder.decode('{"a": 1} extra')

    def test_unclosed_object(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError):
            decoder.decode('{"a": 1')

    def test_unclosed_array(self):
        decoder = JSONDecoder()
        with pytest.raises(TokenizeError):
            decoder.decode("[1, 2, 3")


class TestWhitespaceHandling:
    """Testy obsługi whitespace"""

    def test_leading_whitespace(self):
        decoder = JSONDecoder()
        result = decoder.decode('   {"a": 1}')
        assert result == {"a": 1}

    def test_trailing_whitespace(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"a": 1}   ')
        assert result == {"a": 1}

    def test_whitespace_between_elements(self):
        decoder = JSONDecoder()
        result = decoder.decode('{ "a" : 1 , "b" : 2 }')
        assert result == {"a": 1, "b": 2}

    def test_multiline_json(self):
        decoder = JSONDecoder()
        json_str = """
        {
            "name": "test",
            "value": 123
        }
        """
        result = decoder.decode(json_str)
        assert result == {"name": "test", "value": 123}


class TestEscapeSequences:
    """Testy escape sequences w stringach"""

    def test_escaped_quotes(self):
        decoder = JSONDecoder()
        result = decoder.decode(r'{"text": "He said \"Hello\""}')
        assert result["text"] == 'He said "Hello"'

    def test_escaped_backslash(self):
        decoder = JSONDecoder()
        result = decoder.decode(r'{"path": "C:\\Users\\test"}')
        assert result["path"] == "C:\\Users\\test"

    def test_escaped_newline(self):
        decoder = JSONDecoder()
        result = decoder.decode(r'{"text": "line1\nline2"}')
        assert result["text"] == "line1\nline2"

    def test_unicode_escape(self):
        decoder = JSONDecoder()
        result = decoder.decode(r'{"text": "\u0041\u0042\u0043"}')
        assert result["text"] == "ABC"


class TestNumberParsing:
    """Testy szczegółowe parsowania liczb"""

    def test_integer_types(self):
        decoder = JSONDecoder()
        result = decoder.decode("[0, 1, -1, 123, -456]")
        for num in result:
            assert isinstance(num, int)

    def test_float_types(self):
        decoder = JSONDecoder()
        result = decoder.decode("[1.5, -2.7, 3.14159]")
        for num in result:
            assert isinstance(num, float)

    def test_scientific_notation_types(self):
        decoder = JSONDecoder()
        result = decoder.decode("[1e5, 1.5e-3, -2.7E+10]")
        for num in result:
            assert isinstance(num, float)

    def test_zero_variations(self):
        decoder = JSONDecoder()
        result = decoder.decode("[0, 0.0, -0]")
        assert result == [0, 0.0, 0]


class TestEdgeCases:
    """Testy przypadków brzegowych"""

    def test_very_deep_nesting(self):
        decoder = JSONDecoder()
        depth = 50
        json_str = '{"a":' * depth + "null" + "}" * depth
        result = decoder.decode(json_str)
        # Sprawdź głębokość
        current = result
        for _ in range(depth - 1):
            assert "a" in current
            current = current["a"]
        assert current["a"] is None

    def test_large_array(self):
        decoder = JSONDecoder()
        large_array = "[" + ",".join(str(i) for i in range(1000)) + "]"
        result = decoder.decode(large_array)
        assert len(result) == 1000
        assert result[0] == 0
        assert result[-1] == 999

    def test_many_keys_in_object(self):
        decoder = JSONDecoder()
        keys = [f'"key{i}": {i}' for i in range(100)]
        json_str = "{" + ", ".join(keys) + "}"
        result = decoder.decode(json_str)
        assert len(result) == 100
        assert result["key50"] == 50

    def test_empty_string_value(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"empty": ""}')
        assert result["empty"] == ""

    def test_object_with_single_key(self):
        decoder = JSONDecoder()
        result = decoder.decode('{"only": "one"}')
        assert result == {"only": "one"}

    def test_array_with_single_element(self):
        decoder = JSONDecoder()
        result = decoder.decode("[42]")
        assert result == [42]


class TestTraceMode:
    """Testy trybu trace (jeśli będzie wykorzystany)"""

    def test_trace_mode_enabled(self):
        decoder = JSONDecoder(trace=True)
        result = decoder.decode('{"test": 123}')
        assert result == {"test": 123}

    def test_trace_mode_disabled(self):
        decoder = JSONDecoder(trace=False)
        result = decoder.decode('{"test": 123}')
        assert result == {"test": 123}
