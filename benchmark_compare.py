#!/usr/bin/env python3
"""Simple benchmark comparing JSON parse performance.

Usage:
  python benchmark_compare.py --file test_output.json --iterations 2000
  python benchmark_compare.py --size 10000 --iterations 200
"""

from __future__ import annotations

import argparse
import json
import time
from typing import Callable

from json_engine.api import loads as engine_loads

try:
    import orjson  # type: ignore

    HAVE_ORJSON = True
except Exception:
    HAVE_ORJSON = False


def _generate_json(size: int) -> str:
    payload = {
        "users": [
            {
                "id": i,
                "name": f"User {i}",
                "active": i % 2 == 0,
                "score": i * 1.5,
                "tags": ["json", "benchmark", "test"],
                "meta": {"group": i % 5, "flag": i % 3 == 0},
            }
            for i in range(size)
        ]
    }
    return json.dumps(payload)


def _bench(label: str, func: Callable[[str], object], data: str, iterations: int) -> float:
    start = time.perf_counter()
    for _ in range(iterations):
        func(data)
    end = time.perf_counter()
    elapsed = end - start
    print(f"{label:<20} {elapsed:.6f}s total | {elapsed / iterations:.6f}s per")
    return elapsed


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare JSON parse time.")
    parser.add_argument("--file", type=str, default=None, help="JSON file to parse")
    parser.add_argument("--size", type=int, default=1000, help="Generated data size")
    parser.add_argument("--iterations", type=int, default=1000)
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            data = f.read()
    else:
        data = _generate_json(args.size)

    print(f"Data size: {len(data):,} bytes | iterations: {args.iterations}")
    print("---")

    _bench("json_engine", engine_loads, data, args.iterations)
    _bench("json (stdlib)", json.loads, data, args.iterations)

    if HAVE_ORJSON:
        _bench("orjson", lambda s: orjson.loads(s), data, args.iterations)
    else:
        print("orjson not installed - skipped")


if __name__ == "__main__":
    main()
