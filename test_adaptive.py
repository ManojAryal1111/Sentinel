from src.targets.ollama_target import OllamaTarget
from src.probe_loader import load_probes
from src.adaptive import run_adaptive_attack

t = OllamaTarget(model="dolphin-llama3")
probes = load_probes()

probe = next(p for p in probes if p.id == "DIR-004")
print(f"Testing adaptive attack on {probe.id}...\n")

result = run_adaptive_attack(t, probe)
print("\nRESULT:", result)