# Custom JSON Engine

A simple Python project implementing a custom JSON tokenizer, parser, and serializer. Optional GUI demo for visualization.

## Architecture

```text
json_engine_project/
├── json_engine/
│ ├── init.py # package initializer and API export
│ ├── tokenizer.py # core tokenizer implementation
│ ├── parser.py # core parser implementation
│ ├── encoder.py # JSON encoder / serializer
│ └── api.py # public API: loads, dumps, load, dump
├── tests/
│ ├── test_tokenizer.py # basic unit tests for tokenizer
│ └── test_parser.py # basic unit tests for parser
├── README.md
└── LICENSE
```

This structure separates core modules, unit tests, and documentation, preparing the project for further extension (JSON traversal, benchmarking, GUI demo, etc.).

## Installation

```bash
git clone https://github.com/yourusername/custom-json-engine.git
cd custom-json-engine
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## Usage

```python
from json_api import dumps, loads

data = {"hello": "world", "numbers": [1, 2, 3]}
json_str = dumps(data)
print(json_str)

obj = loads(json_str)
print(obj)

# Run tests
python -m pytest -q
python -m pytest tests/test_tokenizer.py  # example test
```

## Contributing

Feel free to fork the project and submit pull requests.
Focus on tokenizer, parser, traversal, tests, benchmarking, and GUI demo.

## License

MIT License
