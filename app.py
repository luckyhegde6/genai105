import os
import time
import glob
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from comfy_client import comfy_generate
from comfy_client import ComfyClient

COMFY_OUTPUT_DIR = r"F:\ComfyUI\output"
POLL_INTERVAL = 1.0
POLL_TIMEOUT = 120.0  # give SD time to render

app = FastAPI(
    title="GenAI ComfyUI API",
    description="Generate AI art via ComfyUI with prompt and negative prompt support.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------- Helper Functions --------------

def get_latest_image_file():
    """Return the most recent PNG in ComfyUI output folder."""
    files = glob.glob(os.path.join(COMFY_OUTPUT_DIR, "*.png"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def wait_for_new_image(previous_file: str | None) -> str | None:
    """Poll until a new stable image appears."""
    start = time.time()
    while time.time() - start < POLL_TIMEOUT:
        new_file = get_latest_image_file()
        if new_file and new_file != previous_file:
            try:
                size1 = os.path.getsize(new_file)
                time.sleep(1)
                size2 = os.path.getsize(new_file)
                if size1 == size2:
                    print(f"✅ Stable file detected: {new_file}")
                    return new_file
            except FileNotFoundError:
                pass
        time.sleep(POLL_INTERVAL)
    print("⚠️ Timeout: No new stable image found.")
    return None

# -------------- API Models --------------

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    seed: Optional[int] = 42

# -------------- Routes --------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_model=dict)
async def generate_image(req: GenerateRequest):
    prev_file = get_latest_image_file()
    print(f"🕐 Previous file: {prev_file}")

    comfy_generate(
        prompt_text=req.prompt,
        negative_prompt=req.negative_prompt or "blurry, low quality, deformed",
        seed=req.seed or 42,
    )

    # Wait for ComfyUI to write the new file
    new_file = wait_for_new_image(prev_file)
    if not new_file:
        raise HTTPException(500, detail="500: Timed out waiting for new image from ComfyUI")

    file_url = f"/images/{os.path.basename(new_file)}"
    return {
        "status": "ok",
        "prompt": req.prompt,
        "image": {"path": file_url, "filename": os.path.basename(new_file)},
    }

@app.get("/images/{filename}")
async def get_generated_image(filename: str):
    filepath = os.path.join(COMFY_OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(filepath)

# -------------- Run App --------------

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)
