import httpx
from src.target import Target

class OllamaTarget(Target):
    def __init__(self, model: str = "dolphin-llama3", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host

    def send(self, prompt: str, context: dict | None = None) -> str:
        response = httpx.post(
            f"{self.host}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["response"]