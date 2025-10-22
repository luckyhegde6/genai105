import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, Dict
import uvicorn
from config import OUTPUT_DIR
from llm_client import generate_prompt
from comfy_client import comfy_generate
from vectorstore import store_style, query_similar, get_collection
import glob

app = FastAPI(
    title="GenAI ComfyUI API",
    description="An API to generate AI art via ComfyUI with prompt and negative prompt support.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Optional: enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class GenerateRequest(BaseModel):
    prompt: str
    concept: str | None = None
    style: Optional[str] = ""
    negative_prompt: Optional[str] = ""
    seed: Optional[int] = None
    steps: Optional[int] = 28
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    use_memory: Optional[bool] = True

from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None

templates = Jinja2Templates(directory="templates")

# Serve images in /static
app.mount("/static", StaticFiles(directory="static"), name="static")

def latest_output_file(pattern="output/generated_image_*.png"):
    files = sorted(glob.glob(pattern), key=os.path.getmtime)
    return files[-1] if files else None

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_model=dict)
async def generate_image(req: GenerateRequest):
    detailed_prompt = f"{req.prompt}"
    image_output = comfy_generate(
        prompt_text=detailed_prompt,
        negative_prompt=req.negative_prompt or "blurry, distorted, low quality",
        seed=req.seed or 42,
    )
    latest_file = latest_output_file("output/generated_image_*.png")
    file_url = f"/static/{os.path.basename(latest_file)}" if latest_file else None
    return {
        "status": "ok",
        "prompt": detailed_prompt,
        "image": image_output,
        "preview_url": file_url,
    }
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
