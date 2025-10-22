# 🧠 Prompt2Image — Local AI Art Generator using ComfyUI + FastAPI

Prompt2Image is a lightweight **local AI image generation system** that combines:

- 🎨 **ComfyUI (Stable Diffusion)** — handles the actual image generation  
- ⚡ **FastAPI backend** — acts as a middle layer to orchestrate prompts, control seed, and serve generated images  
- 🧩 **Frontend (index.html)** — simple UI for entering prompts and previewing results  
- 🧠 *(Optional)* **Ollama or local LLM** — to enhance text prompts automatically  
- 🧮 **ChromaDB (optional)** — for remembering “style embeddings” for consistent generations  

This project turns your machine into a mini local AI image studio.

---

## 🧰 Features

- Text → Image generation via **ComfyUI REST API**
- Support for **negative prompts**, **seed**, and **LLM-enriched prompts**
- Auto-polling to detect when image files are fully written
- Live image preview in the browser
- FastAPI **Swagger UI** at `/docs`
- Works on **Windows** and **macOS**
- Optional integration with **ChromaDB** for “style memory”

---

## ⚙️ Project Structure

```
genai105/
├── app.py                   # FastAPI backend server
├── comfy_client.py          # Handles ComfyUI API requests
├── llm_client.py            # Optional: Ollama or local LLM integration
├── vectorstore.py           # Optional: ChromaDB vector memory
├── templates/
│   └── index.html           # Web frontend
├── workflows/
│   └── base_workflow.json   # ComfyUI workflow template
├── static/
│   └── (auto-served images go here)
├── config.py
├── requirements.txt
└── README.md
```

---

## 🧩 Prerequisites

### 🪟 For Windows
- **Python 3.10+**
- **Git**
- **ComfyUI (Standalone)**  
  Download from: https://github.com/comfyanonymous/ComfyUI/releases  
  Extract to: `C:\Users\<you>\ComfyUI` or `F:\ComfyUI`
- **Model files**:
  Place your Stable Diffusion model here:
  ```
  F:\ComfyUI\models\checkpoints\v1-5-pruned-emaonly-fp16.safetensors
  ```

### 🍎 For macOS
- Install [Homebrew](https://brew.sh/)
- Run:
  ```bash
  brew install python3 git
  ```
- Download ComfyUI:
  ```bash
  git clone https://github.com/comfyanonymous/ComfyUI.git
  cd ComfyUI
  ```
- Install dependencies:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
- Download the **same model** (`v1-5-pruned-emaonly-fp16.safetensors`) into:
  ```
  ./models/checkpoints/
  ```

---

## 🧩 Installing and Running Prompt2Image

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/prompt2image.git
cd prompt2image
```

### 2. Create a virtual environment
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
fastapi
uvicorn
jinja2
requests
httpx
pydantic
chromadb
```

---

## 🧠 Setting Up ComfyUI (Windows/Mac)

1. Launch ComfyUI:
   ```bash
   python main.py --port 8188
   ```
   or if you have the standalone app, simply run:
   ```
   ComfyUI.exe
   ```
2. Verify it’s running by visiting:
   ```
   http://127.0.0.1:8188
   ```
   You should see the ComfyUI web interface.

3. Make sure your `base_workflow.json` matches your setup.
   - Open ComfyUI.
   - Build a simple text-to-image workflow.
   - Save it as `base_workflow.json` and place it in `workflows/`.

4. Verify your checkpoint name in `base_workflow.json` matches your model file:
   ```json
   "ckpt_name": "v1-5-pruned-emaonly-fp16.safetensors"
   ```

---

## 🚀 Running the FastAPI Backend

With ComfyUI already running on port 8188:

```bash
uvicorn app:app --reload --port 9000
```

You should see logs like:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9000
```

---

## 🖥️ Using the Web UI

Now open:
```
http://127.0.0.1:9000/
```

You’ll see a simple prompt form.

You can also test the API directly via:
```
http://127.0.0.1:9000/docs
```

---

## 🧩 Output

Generated images are stored in:
```
F:\ComfyUI\output\
```
and automatically served at:
```
http://127.0.0.1:9000/images/<filename>.png
```

---

## 🧠 Optional: Add LLM prompt enhancer

Install Ollama and run:
```bash
ollama run llama3
```

Then modify `llm_client.py` accordingly.

---

## 🧮 Optional: Style Memory with ChromaDB

```python
from vectorstore import store_style, query_similar
store_style("ghibli_warm", "anime, soft light, cherry blossoms, elegant harmony")
```

---

## 🧰 Troubleshooting

| Issue | Fix |
|-------|-----|
| **Timed out waiting for image** | Increase `POLL_TIMEOUT` in `app.py`. |
| **Model not found** | Verify checkpoint filename in workflow. |
| **No image displayed** | Check ComfyUI output folder path. |

---

## 🧩 Example Workflow Template

`workflows/base_workflow.json`
```json
{
  "prompt": {
    "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "v1-5-pruned-emaonly-fp16.safetensors"}},
    "2": {"class_type": "CLIPTextEncode", "inputs": {"text": "default prompt", "clip": ["1", 1]}},
    "3": {"class_type": "CLIPTextEncode", "inputs": {"text": "negative prompt", "clip": ["1", 1]}},
    "7": {"class_type": "EmptyLatentImage", "inputs": {"width": 512, "height": 512, "batch_size": 1}},
    "4": {"class_type": "KSampler", "inputs": {"seed": 42, "steps": 20, "cfg": 8.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0, "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["7", 0]}},
    "5": {"class_type": "VAEDecode", "inputs": {"samples": ["4", 0], "vae": ["1", 2]}},
    "6": {"class_type": "SaveImage", "inputs": {"images": ["5", 0], "filename_prefix": "generated_image"}}
  }
}
```

---

## 🧩 Future Upgrades

- [ ] WebSocket integration for real-time progress  
- [ ] Async queue for multi-request handling  
- [ ] Frontend upgrade (React or Svelte UI)  
- [ ] Image history viewer  
- [ ] CLIP-based style embeddings

---

## 🏁 Summary

✅ ComfyUI generates  
✅ FastAPI orchestrates  
✅ HTML UI visualizes  

Your system is now a **self-contained local AI art generator** — fully open, private, and infinitely customizable.

# Happy Art Making! 🎉✨

## Example:
Prompt
```
(ultra realistic portrait:1.3), (elegant woman in crimson silk dress:1.2)
```
Result
```
{
  "status": "ok",
  "prompt": "(ultra realistic portrait:1.3), (elegant woman in crimson silk dress:1.2)",
  "image": {
    "path": "/images/generated_image_00003_.png",
    "filename": "generated_image_00003_.png"
  }
}
```
### Screenshots 
<img width="753" height="717" alt="image" src="https://github.com/user-attachments/assets/6b32c498-259e-49ab-8ee8-b4a9e5bcc39c" />

ComfyUI
<img width="1417" height="770" alt="image" src="https://github.com/user-attachments/assets/08cb1656-e16a-4e04-a6b4-2eab9c3aac62" />

