from typing import Any, TextIO
from .parser import JSONDecoder
from .encoder import JSONEncoder


def loads(s: str, trace: bool = False) -> Any:
    decoder = JSONDecoder(trace=trace)
    return decoder.decode(s)


def dumps(obj: Any) -> str:
    return JSONEncoder().encode(obj)


def load(fp: TextIO, trace: bool = False) -> Any:
    return loads(fp.read(), trace=trace)


def dump(obj: Any, fp: TextIO) -> None:
    fp.write(dumps(obj))
