import typer
from src.targets.ollama_target import OllamaTarget
from src.probe_loader import load_probes
from src.judge import judge_response
from src.adaptive import run_adaptive_attack
from src.baseline import save_baseline, load_baseline, diff_results  # UPDATED

app = typer.Typer()

@app.command()
def scan(target: str = "ollama:dolphin-llama3", adaptive: bool = False, gate: bool = False):
    backend, model = target.split(":")
    if backend == "ollama":
        t = OllamaTarget(model=model)
    else:
        raise typer.BadParameter(f"Unsupported target backend: {backend}")

    probes = load_probes()
    typer.echo(f"Loaded {len(probes)} probes. Running scan against {target}...\n")

    old_baseline = load_baseline()  # NEW — load what the last run looked like, BEFORE we overwrite it
    current_results = {}

    for probe in probes:
        if adaptive:
            result = run_adaptive_attack(t, probe)
            status = f"FAIL (vuln found via {result['turns_used']}-turn adaptive attack)" if result["success"] else f"PASS (resisted {result['turns_used']} turns)"
            typer.echo(f"[{probe.id}] {probe.category} — {status}")
            with open(f"reports/{probe.id}_raw.txt", "w", encoding="utf-8") as f:
                f.write(
                    f"PAYLOAD (original):\n{probe.payload}\n\n"
                    f"FINAL MUTATED PROMPT:\n{result['final_prompt']}\n\n"
                    f"FINAL RESPONSE:\n{result['final_response']}\n\n"
                    f"TURNS USED: {result['turns_used']}\n"
                    f"SUCCESS: {result['success']}\n"
                    f"JUDGE REASONING: {result['reasoning']}\n"
                )
        else:
            response = t.send(probe.payload)
            verdict = judge_response(probe.payload, response)
            status = "FAIL (vuln found)" if verdict["verdict"] == "COMPLY" else "PASS"
            typer.echo(f"[{probe.id}] {probe.category} — {status}")
            with open(f"reports/{probe.id}_raw.txt", "w", encoding="utf-8") as f:
                f.write(f"PAYLOAD:\n{probe.payload}\n\nRESPONSE:\n{response}\n\nJUDGE VERDICT: {verdict['verdict']}\nJUDGE REASONING: {verdict['reasoning']}\n")

        current_results[probe.id] = status

    regressions = diff_results(old_baseline, current_results)  # NEW

    if regressions:
        typer.echo(f"\n⚠ REGRESSIONS DETECTED: {', '.join(regressions)}")
    else:
        typer.echo(f"\nNo regressions detected.")

    save_baseline(current_results)
    typer.echo(f"Baseline saved to baseline.json")

    if gate and regressions:  # NEW — this is what makes it a CI "gate"
        typer.echo(f"\nGate check FAILED — exiting with error code.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()