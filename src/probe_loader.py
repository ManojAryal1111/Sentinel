import yaml
from pathlib import Path
from src.probe import AttackProbe

def load_probes(probes_dir: str = "attacks/probes") -> list[AttackProbe]:
    probes = []
    for path in Path(probes_dir).glob("*.yaml"):
        with open(path) as f:
            data = yaml.safe_load(f)
            probes.append(AttackProbe(**data))
    return probes