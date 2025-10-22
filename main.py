from llm_client import generate_prompt
from comfy_client import generate_image

def main():
    concept = input("Enter your concept: ")
    print("🧠 Generating detailed prompt using Ollama...")
    prompt = generate_prompt(concept)
    print(f"Prompt:\n{prompt}\n")

    print("🎨 Sending prompt to ComfyUI for image generation...")
    generate_image(prompt)

if __name__ == "__main__":
    main()
