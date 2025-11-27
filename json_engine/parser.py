from typing import Any, List
from .tokenizer import tokenize, TokenizeError, Token


class JSONDecoder:
    def __init__(self, trace: bool = False):
        self.trace = trace
        self.tokens: List[Token] = []
        self.pos = 0

    def _peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token('EOF', '', -1, -1)

    def _next(self):
        tok = self._peek()
        self.pos += 1
        return tok

    def decode(self, s: str) -> Any:
        if s is None or s == '':
            raise ValueError("Empty string")

        self.tokens = list(tokenize(s))
        self.pos = 0

        def parse_value():
            tok = self._peek()
            if tok.type == '{':
                return parse_object()
            if tok.type == '[':
                return parse_array()
            if tok.type == 'STRING':
                self._next()
                return tok.value
            if tok.type == 'NUMBER':
                self._next()
                if '.' in tok.value or 'e' in tok.value or 'E' in tok.value:
                    return float(tok.value)
                try:
                    return int(tok.value)
                except Exception:
                    return float(tok.value)
            if tok.type == 'TRUE':
                self._next()
                return True
            if tok.type == 'FALSE':
                self._next()
                return False
            if tok.type == 'NULL':
                self._next()
                return None
            raise TokenizeError("Unexpected token", tok.line, tok.column)

        def parse_object():
            start_tok = self._next()
            obj = {}
            tok = self._peek()
            if tok.type == '}':
                self._next()
                return obj
            while True:
                key_tok = self._peek()
                if key_tok.type != 'STRING':
                    raise TokenizeError("Expected string as object key", key_tok.line, key_tok.column)
                self._next()
                colon_tok = self._peek()
                if colon_tok.type != ':':
                    raise TokenizeError("Expected ':' after object key", colon_tok.line, colon_tok.column)
                self._next()
                value = parse_value()
                obj[key_tok.value] = value
                sep = self._peek()
                if sep.type == ',':
                    self._next()
                    continue
                if sep.type == '}':
                    self._next()
                    break
                raise TokenizeError("Expected ',' or '}' in object", sep.line, sep.column)
            return obj

        def parse_array():
            self._next()
            arr = []
            tok = self._peek()
            if tok.type == ']':
                self._next()
                return arr
            while True:
                arr.append(parse_value())
                sep = self._peek()
                if sep.type == ',':
                    self._next()
                    continue
                if sep.type == ']':
                    self._next()
                    break
                raise TokenizeError("Expected ',' or ']' in array", sep.line, sep.column)
            return arr

        result = parse_value()
        if self.pos != len(self.tokens):
            remaining = self._peek()
            raise TokenizeError("Extra data after valid JSON", remaining.line, remaining.column)
        return result
