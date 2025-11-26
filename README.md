# Custom JSON Engine

A simple Python project implementing a custom JSON tokenizer, parser, and serializer. Optional GUI demo for visualization.

## Project Status

**Completed**
- Repository and environment setup
- MIT license integration
- Tokenizer design

**In Progress**
- Core parser
- JSON traversal module

**Planned**
- Public API usability
- Benchmarking and performance tests
- Optional GUI demo

## Installation

```bash
git clone https://github.com/yourusername/custom-json-engine.git
cd custom-json-engine
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## Usage

from json_api import dumps, loads

data = {"hello": "world", "numbers": [1, 2, 3]}
json_str = dumps(data)
print(json_str)

obj = loads(json_str)
print(obj)

## Contributing

Feel free to fork the project and submit pull requests.
Focus on tokenizer, parser, traversal, tests, benchmarking, and GUI demo.

## License

MIT License
