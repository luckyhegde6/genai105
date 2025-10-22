import requests
import json

COMFY_API = "http://127.0.0.1:8188/api/prompt"

def comfy_generate(prompt_text, negative_prompt="", seed=42):
    # Load a working workflow template
    with open("workflows/base_workflow.json", "r") as f:
        workflow = json.load(f)

    # Replace the text prompt node values
    for node_id, node in workflow.get("prompt", {}).items():
        if node["class_type"] == "CLIPTextEncode":
            node["inputs"]["text"] = prompt_text

    if "prompt" in workflow:
     payload = workflow
    else:
     payload = {"prompt": workflow}
     print("\n=== PAYLOAD TO COMFYUI ===")
    print(json.dumps(payload, indent=2)[:2000])
    print("===========================\n")
    response = requests.post(COMFY_API, json=payload)
    print("\n===COMFYUI Response===")
    print(json.dumps(response.json(), indent=2)[:2000])
    print("===========================\n")
    if response.status_code != 200:
            print("===COMFYUI ERROR===")
            print(response.text)
            raise RuntimeError(f"ComfyUI generation failed: {response.status_code} - {response.text}")
    return response.json()
