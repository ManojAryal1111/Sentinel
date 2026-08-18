import httpx
from src.target import Target

class APITarget(Target):
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def send(self, prompt: str, context: dict | None = None) -> str:
        response = httpx.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"prompt": prompt},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["response"]