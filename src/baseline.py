import json
import os

def save_baseline(results: dict, path: str = "baseline.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def load_baseline(path: str = "baseline.json") -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}