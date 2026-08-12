import typer
from src.targets.ollama_target import OllamaTarget

app = typer.Typer()

@app.command()
def scan(target: str = "ollama:dolphin-llama3", prompt: str = "Hello, who are you?"):
    backend, model = target.split(":")
    if backend == "ollama":
        t = OllamaTarget(model=model)
    else:
        raise typer.BadParameter(f"Unsupported target backend: {backend}")
    result = t.send(prompt)
    typer.echo(result)

if __name__ == "__main__":
    app()