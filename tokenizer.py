class Token:
    def __init__(self, type_: str, value: str, line: int, column: int):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"


class TokenizeError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")


def tokenize(json_string: str):
    import re

    i = 0
    line = 1
    col = 1
    length = len(json_string)

    number_regex = re.compile(r'-?\d+(\.\d+)?([eE][+-]?\d+)?')
    keywords = {'true': True, 'false': False, 'null': None}

    while i < length:
        char = json_string[i]

        if char in ' \t\r':
            i += 1
            col += 1
            continue
        elif char == '\n':
            i += 1
            line += 1
            col = 1
            continue
        elif char in '{}[]:,':
            yield Token(char, char, line, col)
            i += 1
            col += 1
            continue
        elif char == '"':
            # parse string
            start_col = col
            i += 1
            col += 1
            value = ''
            while i < length:
                if json_string[i] == '"':
                    i += 1
                    col += 1
                    break
                elif json_string[i] == '\\':
                    i += 1
                    col += 1
                    if i < length:
                        value += json_string[i]
                        i += 1
                        col += 1
                else:
                    value += json_string[i]
                    i += 1
                    col += 1
            else:
                raise TokenizeError("Unterminated string", line, start_col)
            yield Token('STRING', value, line, start_col)
        elif char.isdigit() or char == '-':
            # parse number
            start_col = col
            match = number_regex.match(json_string[i:])
            if match:
                num_str = match.group(0)
                i += len(num_str)
                col += len(num_str)
                yield Token('NUMBER', num_str, line, start_col)
            else:
                raise TokenizeError("Invalid number", line, col)
        else:
            # parse keywords: true, false, null
            start_col = col
            for kw in keywords:
                if json_string.startswith(kw, i):
                    i += len(kw)
                    col += len(kw)
                    yield Token(kw.upper(), kw, line, start_col)
                    break
            else:
                raise TokenizeError(f"Unexpected character '{char}'", line, col)
