import requests
import json
import httpx

COMFY_API = "http://127.0.0.1:8188/api/prompt"


class ComfyClient:
    def __init__(self, base_url='http://127.0.0.1:8188/api'):
        self.base_url = base_url
        self.session = httpx.AsyncClient()

    async def get_images(self):
        response = await self.session.get(f"{self.base_url}/images")
        response.raise_for_status()
        return response.json()


def comfy_generate(prompt_text, negative_prompt="", seed=42):
    # Load base workflow template
    with open("workflows/base_workflow.json", "r") as f:
        workflow = json.load(f)

    # Safely get the inner prompt dictionary
    nodes = workflow.get("prompt", workflow)

    # Inject prompts into their correct CLIP nodes
    for node_id, node in nodes.items():
        if node["class_type"] == "CLIPTextEncode":
            # Heuristic: decide which node is negative based on its ID
            if node_id in ["3", "neg", "negative", "n1"]:  # Common naming patterns
                node["inputs"]["text"] = negative_prompt or "low quality, blurry, distorted"
            else:
                node["inputs"]["text"] = prompt_text or "a beautiful digital artwork"

        # Also inject seed if a KSampler node exists
        if node["class_type"] == "KSampler":
            node["inputs"]["seed"] = seed

    payload = workflow if "prompt" in workflow else {"prompt": workflow}

    # Debug logging
    print("\n=== PAYLOAD TO COMFYUI ===")
    print(json.dumps(payload, indent=2)[:2000])
    print("===========================\n")

    # Send request
    response = requests.post(COMFY_API, json=payload)

    # Handle and log response
    try:
        data = response.json()
        print("\n===COMFYUI Response===")
        print(json.dumps(data, indent=2)[:2000])
        print("===========================\n")
    except Exception:
        print("\n===COMFYUI RAW RESPONSE===")
        print(response.text)
        print("===========================\n")
        raise RuntimeError(f"ComfyUI returned non-JSON response: {response.text}")

    if response.status_code != 200:
        raise RuntimeError(f"ComfyUI generation failed: {response.status_code} - {response.text}")

    return data
