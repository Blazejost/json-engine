from tokenizer import tokenize, TokenizeError


def test_simple_json():
    json_str = '{"a":1,"b":true}'
    tokens = list(tokenize(json_str))
    assert [t.type for t in tokens] == ['{', 'STRING', ':', 'NUMBER', ',', 'STRING', ':', 'TRUE', '}']
    print("Simple JSON test passed.")

def test_nested_json():
    json_str = '{"nested":{"x":10}}'
    tokens = list(tokenize(json_str))
    assert [t.type for t in tokens] == ['{', 'STRING', ':', '{', 'STRING', ':', 'NUMBER', '}', '}']
    print("Nested JSON test passed.")

def test_array_json():
    json_str = '[1,2,3,null]'
    tokens = list(tokenize(json_str))
    assert [t.type for t in tokens] == ['[', 'NUMBER', ',', 'NUMBER', ',', 'NUMBER', ',', 'NULL', ']']
    print("Array JSON test passed.")

def test_unterminated_string():
    json_str = '{"a": "oops}'
    try:
        tokens = list(tokenize(json_str))
    except TokenizeError:
        print("Unterminated string test passed.")
    else:
        raise AssertionError("Unterminated string not caught!")

if __name__ == "__main__":
    test_simple_json()
    test_nested_json()
    test_array_json()
    test_unterminated_string()
