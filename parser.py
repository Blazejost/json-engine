import io
from typing import Any, TextIO, Union

class JSONTokenizer:
    """
    Odpowiada za skanowanie tekstu (Zadanie T-04).
    Tu trafi logika rozbijania stringa na tokeny: {, }, [, ], "string", 123, itd.
    """
    def __init__(self, text: str):
        self.text = text
        self.index = 0

    # Placeholder - w pełnej wersji tu będzie logika skanowania
    def next_token(self):
        pass

class JSONDecoder:
    """
    Odpowiada za deserializację (Parsowanie).
    Przekształca tekst JSON na obiekty Pythona.
    """
    def __init__(self, trace: bool = False):
        self.trace = trace  # Obsługa funkcjonalności trasowania

    def decode(self, s: str) -> Any:
        # Tutaj nastąpi użycie Tokenizera i budowanie obiektów
        # Na potrzeby demonstracji API używamy wbudowanego eval (UWAGA: tylko demo!)
        # W finalnej wersji tutaj będzie Twój algorytm parsera.
        if not s:
            raise ValueError("Empty string")
        
        # Symulacja parsowania prostych typów dla testu API
        if s == "true": return True
        if s == "false": return False
        if s == "null": return None
        
        # Właściwa implementacja użyje tutaj JSONTokenizer
        # tokenizer = JSONTokenizer(s)
        # ... logika parsowania ...
        return "Symulacja obiektu (tu będzie wynik parsera)"

class JSONEncoder:
    """
    Odpowiada za serializację.
    Przekształca obiekty Pythona na tekst JSON.
    """
    def encode(self, obj: Any) -> str:
        # Rekurencyjna obsługa typów danych
        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            return f'"{obj}"' # Uproszczony escaping
        elif isinstance(obj, list):
            items = [self.encode(item) for item in obj]
            return "[" + ", ".join(items) + "]"
        elif isinstance(obj, dict):
            items = [f'{self.encode(k)}: {self.encode(v)}' for k, v in obj.items()]
            return "{" + ", ".join(items) + "}"
        else:
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# --- PUBLICZNE API (Zgodne ze standardem Python) ---

def dumps(obj: Any, trace: bool = False) -> str:
    """
    Serializacja obiektu do stringa (Serialize).
    """
    encoder = JSONEncoder()
    return encoder.encode(obj)

def loads(s: str, trace: bool = False) -> Any:
    """
    Deserializacja stringa do obiektu (Deserialize).
    """
    decoder = JSONDecoder(trace=trace)
    return decoder.decode(s)

def dump(obj: Any, fp: TextIO, trace: bool = False) -> None:
    """
    Serializacja obiektu bezpośrednio do pliku (strumienia).
    """
    # Wykorzystujemy implementację dumps, ale piszemy do pliku
    # To pozwala zachować DRY (Don't Repeat Yourself) [cite: 33, 37]
    s = dumps(obj, trace=trace)
    fp.write(s)

def load(fp: TextIO, trace: bool = False) -> Any:
    """
    Deserializacja obiektu bezpośrednio z pliku (strumienia).
    """
    # Czytamy całość pliku i przekazujemy do loads
    return loads(fp.read(), trace=trace)

# --- PRZYKŁAD UŻYCIA (TEST) ---

if __name__ == "__main__":
    # 1. Dane testowe
    data = {
        "projekt": "Wlasny Silnik JSON",
        "wersja": 1.0,
        "autorzy": ["Maxim", "Blazej"],
        "aktywny": True,
        "meta": None
    }

    print("--- Test Serializacji (dumps) ---")
    json_str = dumps(data)
    print(f"Wynik: {json_str}")

    print("\n--- Test Zapisu do pliku (dump) ---")
    with open("test_output.json", "w") as f:
        dump(data, f)
    print("Zapisano do pliku test_output.json")

    print("\n--- Test API Deserializacji (loads - symulacja) ---")
    # W tej fazie zwraca placeholder, bo nie piszemy tu pełnego parsera
    obj = loads("null") 
    print(f"Wczytano: {obj}")