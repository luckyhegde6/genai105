import requests
from typing import Optional
from config import OLLAMA_API, OLLAMA_MODEL

def generate_prompt(concept: str, style_hint: Optional[str] = None) -> str:
    """
    Ask local Ollama to expand a short concept into a long, detailed image prompt.
    Returns the generated prompt text.
    """
    # Keep payload small and explicit; adapt to your local Ollama API shape
    prompt = f"Create a detailed, evocative image prompt for a text-to-image model. Concept: {concept}."
    if style_hint:
        prompt += f" Add stylistic modifiers: {style_hint}."
    # You can craft a system / instructions here for consistent output
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "max_tokens": 4000,
        "stream": False
    }
    r = requests.post(OLLAMA_API, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    # Ollama JSON shape may vary; try to get common keys used in community builds
    # Expect either data["response"] or data["text"]
    txt = data.get("response") or data.get("text") or ""
    return txt.strip()
