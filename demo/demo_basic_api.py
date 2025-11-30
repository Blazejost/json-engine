from json_engine.api import loads, dumps, JSONError


def main():
    print("=== Basic JSON API Demonstration ===\n")

    sample = {
        "message": "hello",
        "numbers": [1, 2, 3],
        "flags": {"active": True, "debug": False},
        "value": 51.7
    }

    print("Input Python object:")
    print(sample, "\n")

    json_str = dumps(sample)
    print("Serialized JSON:")
    print(json_str, "\n")

    parsed = loads(json_str)
    print("Parsed back to Python:")
    print(parsed, "\n")

    print("=== Error Handling Example ===\n")
    bad_json = '{"a": 1, "b": [1, 2,, 3]}'

    try:
        loads(bad_json)
    except JSONError as e:
        print("Error captured correctly:", e)

if __name__ == "__main__":
    main()
