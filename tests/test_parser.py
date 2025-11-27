from json_engine.api import loads, dumps
from json_engine.tokenizer import TokenizeError


def test_loads_simple():
    s = '{"a": 1, "b": [true, null, 3]}'
    obj = loads(s)
    assert obj['a'] == 1
    assert obj['b'][0] is True
    assert obj['b'][1] is None
    print('test_loads_simple OK')


def test_parser_error():
    try:
        loads('{"a": 1 1}')
    except TokenizeError as e:
        print('test_parser_error OK', e)
    else:
        raise AssertionError('Expected TokenizeError')
