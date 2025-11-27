import re
from typing import Generator

class Token:
    def __init__(self, type_: str, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r}, line={self.line}, col={self.column})"


class TokenizeError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"{message} at line {line}, column {column}")
        self.line = line
        self.column = column


def tokenize(json_string: str) -> Generator[Token, None, None]:
    i = 0
    line = 1
    col = 1
    length = len(json_string)

    number_regex = re.compile(r'-?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?')
    keywords = {'true': 'TRUE', 'false': 'FALSE', 'null': 'NULL'}

    while i < length:
        ch = json_string[i]

        if ch in ' \t\r':
            i += 1
            col += 1
            continue
        if ch == '\n':
            i += 1
            line += 1
            col = 1
            continue

        if ch in '{}[]:,':
            yield Token(ch, ch, line, col)
            i += 1
            col += 1
            continue

        if ch == '"':
            start_col = col
            i += 1
            col += 1
            value_chars = []
            while i < length:
                c = json_string[i]
                if c == '"':
                    i += 1
                    col += 1
                    break
                if c == '\\':
                    i += 1
                    col += 1
                    if i >= length:
                        raise TokenizeError("Unterminated escape sequence", line, col)
                    esc = json_string[i]
                    if esc == 'n':
                        value_chars.append('\n')
                    elif esc == 'r':
                        value_chars.append('\r')
                    elif esc == 't':
                        value_chars.append('\t')
                    elif esc == 'b':
                        value_chars.append('\b')
                    elif esc == 'f':
                        value_chars.append('\f')
                    elif esc in ('"', '\\', '/'):
                        value_chars.append(esc)
                    elif esc == 'u':
                        hex_seq = json_string[i+1:i+5]
                        if len(hex_seq) < 4 or not all(c in '0123456789abcdefABCDEF' for c in hex_seq):
                            raise TokenizeError("Invalid unicode escape", line, col)
                        value_chars.append(chr(int(hex_seq, 16)))
                        i += 4
                        col += 4
                    else:
                        value_chars.append(esc)
                    i += 1
                    col += 1
                    continue
                else:
                    value_chars.append(c)
                    i += 1
                    col += 1
            else:
                raise TokenizeError("Unterminated string", line, start_col)
            yield Token('STRING', ''.join(value_chars), line, start_col)
            continue

        if ch == '-' or ch.isdigit():
            start_col = col
            m = number_regex.match(json_string[i:])
            if not m:
                raise TokenizeError("Invalid number", line, col)
            num_str = m.group(0)
            yield Token('NUMBER', num_str, line, start_col)
            i += len(num_str)
            col += len(num_str)
            continue

        matched_kw = None
        for kw, ttype in keywords.items():
            if json_string.startswith(kw, i):
                matched_kw = (kw, ttype)
                break
        if matched_kw:
            kw, ttype = matched_kw
            start_col = col
            yield Token(ttype, kw, line, start_col)
            i += len(kw)
            col += len(kw)
            continue

        raise TokenizeError(f"Unexpected character {ch!r}", line, col)
