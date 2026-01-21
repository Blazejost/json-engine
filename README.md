# Custom JSON Engine

Custom JSON tokenizer, parser, and encoder with a CLI demo, benchmarking, and comprehensive tests.

## Project Structure

```text
json-engine/
├── json_engine/              # Core package
│   ├── __init__.py
│   ├── tokenizer.py
│   ├── parser.py
│   ├── encoder.py
│   └── api.py
├── tests/                    # Unit + integration tests
├── documentation/            # Project docs and diagrams
├── benchmark_compare.py      # Benchmark vs stdlib/orjson
├── main.py                   # CLI demo
├── pyproject.toml
└── README.md
```

## Setup (uv recommended)

```bash
uv sync --extra dev
```

## Usage (Python API)

```python
from json_engine.api import dumps, loads

data = {"hello": "world", "numbers": [1, 2, 3]}
json_str = dumps(data)
print(json_str)

obj = loads(json_str)
print(obj)
```

## CLI Demo ("WOW")

```bash
# Interactive mode
uv run python main.py --demo

# Samples
uv run python main.py --samples

# Parse JSON from CLI
uv run python main.py --parse '{"a": 1, "b": [true, null]}'

# Show tokenizer output
uv run python main.py --parse '{"a": 1}' --tokens
```

## Tests

```bash
uv run pytest -v
```

## Coverage Report (HTML)

```bash
uv run pytest --cov=json_engine --cov-report=html
xdg-open htmlcov/index.html
```

## Benchmark

```bash
uv run python benchmark_compare.py --size 2000 --iterations 300
```

## Documentation

- Project structure and design: [documentation/PROJECT_STRUKTURA.md](documentation/PROJECT_STRUKTURA.md)
- Testing guide: [documentation/README_TESTING.md](documentation/README_TESTING.md)

## License

MIT License
