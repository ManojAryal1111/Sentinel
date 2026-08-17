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

def diff_results(old: dict, new: dict) -> list[str]:
    regressions = []
    for probe_id, new_status in new.items():
        old_status = old.get(probe_id, "PASS")
        if "PASS" in old_status and "FAIL" in new_status:
            regressions.append(probe_id)
    return regressions