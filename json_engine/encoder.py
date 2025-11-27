from typing import Any


class JSONEncoder:
    def encode(self, obj: Any) -> str:
        if obj is None:
            return "null"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, int):
            return str(obj)
        if isinstance(obj, float):
            return str(obj)
        if isinstance(obj, str):
            esc = obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            return f'"{esc}"'
        if isinstance(obj, list):
            return "[" + ", ".join(self.encode(x) for x in obj) + "]"
        if isinstance(obj, dict):
            items = []
            for k, v in obj.items():
                if not isinstance(k, str):
                    raise TypeError("Keys must be strings")
                items.append(f"{self.encode(k)}: {self.encode(v)}")
            return "{" + ", ".join(items) + "}"
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
