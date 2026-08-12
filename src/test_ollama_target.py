from src.targets.ollama_target import OllamaTarget

def test_ollama_target_returns_response():
    target = OllamaTarget(model="dolphin-llama3")
    result = target.send("Say hello in one word.")
    assert isinstance(result, str)
    assert len(result) > 0