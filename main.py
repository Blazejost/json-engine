from __future__ import annotations

import argparse
from typing import Any

from json_engine.api import JSONError, dumps, loads
from json_engine.tokenizer import tokenize


def _sample_payloads() -> list[dict[str, Any]]:
    return [
        {
            "name": "Alice",
            "age": 30,
            "active": True,
            "skills": ["python", "json"],
        },
        {
            "project": "json-engine",
            "version": "1.0.0",
            "stats": {"tests": 250, "coverage": 95.08},
        },
    ]


def _print_tokens(json_text: str) -> None:
    tokens = list(tokenize(json_text))
    print("Tokens:")
    for tok in tokens:
        print(f"  {tok}")


def _parse_and_show(json_text: str, *, show_tokens: bool) -> None:
    if show_tokens:
        _print_tokens(json_text)
    data = loads(json_text)
    print("Parsed (Python):")
    print(data)
    print("Re-encoded JSON:")
    print(dumps(data))


def _demo_interactive() -> None:
    print("JSON Engine Demo (interactive)")
    print("Type JSON and press Enter. Empty line to exit.")
    print("Tip: use --tokens to show tokenizer output.")
    while True:
        try:
            json_text = input("json> ").strip()
        except EOFError:
            break
        if not json_text:
            break
        try:
            _parse_and_show(json_text, show_tokens=False)
        except JSONError as exc:
            print(f"Error: {exc}")


def _demo_samples() -> None:
    print("JSON Engine Demo (samples)")
    for idx, payload in enumerate(_sample_payloads(), start=1):
        print(f"Sample {idx}:")
        encoded = dumps(payload)
        print(encoded)
        print("Round-trip:")
        print(loads(encoded))
        print("-")


def main() -> None:
    parser = argparse.ArgumentParser(description="JSON Engine CLI demo")
    parser.add_argument("--demo", action="store_true", help="Run interactive demo")
    parser.add_argument("--samples", action="store_true", help="Run sample demo")
    parser.add_argument("--parse", type=str, help="Parse JSON string")
    parser.add_argument("--file", type=str, help="Parse JSON from file")
    parser.add_argument("--tokens", action="store_true", help="Show tokenizer output")
    args = parser.parse_args()

    if args.demo:
        _demo_interactive()
        return

    if args.samples:
        _demo_samples()
        return

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            json_text = f.read()
        try:
            _parse_and_show(json_text, show_tokens=args.tokens)
        except JSONError as exc:
            print(f"Error: {exc}")
        return

    if args.parse:
        try:
            _parse_and_show(args.parse, show_tokens=args.tokens)
        except JSONError as exc:
            print(f"Error: {exc}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
