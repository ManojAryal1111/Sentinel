import typer
from src.targets.ollama_target import OllamaTarget
from src.probe_loader import load_probes
from src.judge import judge_response

app = typer.Typer()

@app.command()
def scan(target: str = "ollama:dolphin-llama3"):
    backend, model = target.split(":")
    if backend == "ollama":
        t = OllamaTarget(model=model)
    else:
        raise typer.BadParameter(f"Unsupported target backend: {backend}")

    probes = load_probes()
    typer.echo(f"Loaded {len(probes)} probes. Running scan against {target}...\n")

    for probe in probes:
        response = t.send(probe.payload)
        verdict = judge_response(probe.payload, response)

        status = "FAIL (vuln found)" if verdict["verdict"] == "COMPLY" else "PASS"

        typer.echo(f"    → {response[:150]}")
        typer.echo(f"[{probe.id}] {probe.category} — {status}")
        typer.echo(f"    judge: {verdict['reasoning']}\n")

        with open(f"reports/{probe.id}_raw.txt", "w", encoding="utf-8") as f:
            f.write(
                f"PAYLOAD:\n{probe.payload}\n\n"
                f"RESPONSE:\n{response}\n\n"
                f"JUDGE VERDICT: {verdict['verdict']}\n"
                f"JUDGE REASONING: {verdict['reasoning']}\n"
            )

if __name__ == "__main__":
    app()