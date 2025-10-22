# genai105
Image generation using local LLM

# Prompt2Image — Local LLM + ComfyUI + ChromaDB

## Setup
1. Install dependencies:
   python -m venv .venv  
   .venv/Scripts/activate.bat
   pip install -r requirements.txt

2. Start Ollama locally (your Ollama install).
3. Start ComfyUI and verify its REST endpoints (/generate & /status/<id>) — adjust comfy_client.py if different.
4. Edit `.env` from `.env.example` if needed.

5. Run the app:
   uvicorn app:app --reload --port 9000

6. Visit http://localhost:9000 — enter concept, style, negatives, press Generate.

## Notes
- Chroma uses sentence-transformers to compute embeddings. The first time it runs it will download a small model.
- If ComfyUI endpoints differ, update comfy_client.py to match your ComfyUI's API.
