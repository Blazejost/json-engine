import pytest

from json_engine.tokenizer import TokenizeError, tokenize


class TestTokenizerBasics:
    """Testy podstawowych tokenów JSON"""

    def test_empty_object(self):
        tokens = list(tokenize("{}"))
        assert len(tokens) == 2
        assert tokens[0].type == "{"
        assert tokens[1].type == "}"

    def test_empty_array(self):
        tokens = list(tokenize("[]"))
        assert len(tokens) == 2
        assert tokens[0].type == "["
        assert tokens[1].type == "]"

    def test_punctuation_tokens(self):
        tokens = list(tokenize("{}[]:,"))
        assert [t.type for t in tokens] == ["{", "}", "[", "]", ":", ","]

    def test_whitespace_ignored(self):
        tokens = list(tokenize("  {  }  "))
        assert len(tokens) == 2
        assert tokens[0].type == "{"


class TestStringTokens:
    """Testy tokenizacji stringów"""

    def test_simple_string(self):
        tokens = list(tokenize('"hello"'))
        assert len(tokens) == 1
        assert tokens[0].type == "STRING"
        assert tokens[0].value == "hello"

    def test_empty_string(self):
        tokens = list(tokenize('""'))
        assert tokens[0].value == ""

    def test_string_with_spaces(self):
        tokens = list(tokenize('"hello world"'))
        assert tokens[0].value == "hello world"

    def test_escape_sequences(self):
        test_cases = [
            (r'"hello\nworld"', "hello\nworld"),
            (r'"tab\there"', "tab\there"),
            (r'"quote\"here"', 'quote"here'),
            (r'"backslash\\here"', "backslash\\here"),
            (r'"slash\/here"', "slash/here"),
        ]
        for json_str, expected in test_cases:
            tokens = list(tokenize(json_str))
            assert tokens[0].value == expected

    def test_unicode_escape(self):
        tokens = list(tokenize(r'"\u0041\u0042\u0043"'))
        assert tokens[0].value == "ABC"

    def test_unterminated_string(self):
        with pytest.raises(TokenizeError, match="Unterminated string"):
            list(tokenize('"hello'))

    def test_invalid_escape(self):
        # Parser powinien obsłużyć nieznany escape jako literał
        tokens = list(tokenize(r'"\x"'))
        assert tokens[0].value == "x"

    def test_unterminated_escape(self):
        with pytest.raises(TokenizeError, match="Unterminated escape"):
            list(tokenize('"hello\\'))

    def test_invalid_unicode_escape(self):
        with pytest.raises(TokenizeError, match="Invalid unicode escape"):
            list(tokenize(r'"\u123"'))  # Za krótkie
        with pytest.raises(TokenizeError, match="Invalid unicode escape"):
            list(tokenize(r'"\uGGGG"'))  # Nieprawidłowe znaki


class TestNumberTokens:
    """Testy tokenizacji liczb"""

    def test_integer(self):
        tokens = list(tokenize("123"))
        assert tokens[0].type == "NUMBER"
        assert tokens[0].value == "123"

    def test_negative_integer(self):
        tokens = list(tokenize("-456"))
        assert tokens[0].value == "-456"

    def test_zero(self):
        tokens = list(tokenize("0"))
        assert tokens[0].value == "0"

    def test_float(self):
        tokens = list(tokenize("123.456"))
        assert tokens[0].value == "123.456"

    def test_negative_float(self):
        tokens = list(tokenize("-123.456"))
        assert tokens[0].value == "-123.456"

    def test_scientific_notation(self):
        test_cases = ["1e10", "1E10", "1e+10", "1e-10", "1.5e10", "-1.5e-10"]
        for num_str in test_cases:
            tokens = list(tokenize(num_str))
            assert tokens[0].type == "NUMBER"
            assert tokens[0].value == num_str

    def test_leading_zeros_invalid(self):
        # JSON nie pozwala na leading zeros (oprócz samego 0)
        with pytest.raises(TokenizeError):
            list(tokenize("01"))


class TestKeywordTokens:
    """Testy tokenizacji słów kluczowych"""

    def test_true(self):
        tokens = list(tokenize("true"))
        assert tokens[0].type == "TRUE"
        assert tokens[0].value == "true"

    def test_false(self):
        tokens = list(tokenize("false"))
        assert tokens[0].type == "FALSE"
        assert tokens[0].value == "false"

    def test_null(self):
        tokens = list(tokenize("null"))
        assert tokens[0].type == "NULL"
        assert tokens[0].value == "null"


class TestLineAndColumnTracking:
    """Testy śledzenia pozycji w pliku"""

    def test_single_line_positions(self):
        tokens = list(tokenize('{"a": 1}'))
        assert tokens[0].line == 1
        assert tokens[0].column == 1  # {
        assert tokens[1].line == 1
        assert tokens[1].column == 2  # "a"

    def test_multiline_positions(self):
        json_str = '{\n  "key": "value"\n}'
        tokens = list(tokenize(json_str))
        # Pierwszy token { w linii 1, kolumnie 1
        assert tokens[0].line == 1
        assert tokens[0].column == 1
        # Token "key" w linii 2
        assert tokens[1].line == 2
        # Ostatni token } w linii 3
        assert tokens[-1].line == 3

    def test_error_position_reporting(self):
        try:
            list(tokenize('{\n  "key": @@\n}'))
        except TokenizeError as e:
            assert e.line == 2
            assert "@@" in str(e) or "Unexpected" in str(e)


class TestComplexStructures:
    """Testy złożonych struktur JSON"""

    def test_nested_object(self):
        tokens = list(tokenize('{"a": {"b": 1}}'))
        types = [t.type for t in tokens]
        assert "{" in types
        assert "STRING" in types
        assert ":" in types

    def test_array_of_objects(self):
        tokens = list(tokenize('[{"a": 1}, {"b": 2}]'))
        assert tokens[0].type == "["
        assert tokens[-1].type == "]"
        assert len([t for t in tokens if t.type == ","]) >= 1

    def test_mixed_types(self):
        tokens = list(tokenize('[1, "str", true, false, null, 3.14]'))
        types = [t.type for t in tokens if t.type != "," and t.type != "[" and t.type != "]"]
        assert "NUMBER" in types
        assert "STRING" in types
        assert "TRUE" in types
        assert "FALSE" in types
        assert "NULL" in types


class TestErrorHandling:
    """Testy obsługi błędów"""

    def test_unexpected_character(self):
        with pytest.raises(TokenizeError, match="Unexpected character"):
            list(tokenize("@"))

    def test_invalid_number_format(self):
        with pytest.raises(TokenizeError):
            list(tokenize("123."))  # Kropka bez cyfr po niej

    def test_error_contains_position(self):
        try:
            list(tokenize("invalid"))
        except TokenizeError as e:
            assert hasattr(e, "line")
            assert hasattr(e, "column")
            assert e.line > 0
            assert e.column > 0


class TestEdgeCases:
    """Testy przypadków brzegowych"""

    def test_very_long_string(self):
        long_str = '"' + "a" * 10000 + '"'
        tokens = list(tokenize(long_str))
        assert len(tokens[0].value) == 10000

    def test_deeply_nested_brackets(self):
        nested = "[" * 100 + "]" * 100
        tokens = list(tokenize(nested))
        assert len(tokens) == 200

    def test_multiple_newlines(self):
        tokens = list(tokenize('{\n\n\n"key": "value"\n\n}'))
        assert len([t for t in tokens if t.type == "STRING"]) == 2

    def test_tabs_and_spaces(self):
        tokens = list(tokenize('{\t"key":\t\t"value"\t}'))
        assert len(tokens) == 5  # {, "key", :, "value", }
