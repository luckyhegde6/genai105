import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API = os.getenv("OLLAMA_API", "http://localhost:11434/api/generate")
COMFY_API = os.getenv("COMFY_API", "http://127.0.0.1:8188")
SD_MODEL = os.getenv("SD_MODEL", "stable-diffusion-xl-base-1.0")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "static/outputs")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_storage")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nominic-embed-text:latest")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")  # change as needed
