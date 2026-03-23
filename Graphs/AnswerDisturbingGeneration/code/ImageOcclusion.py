import os
import json
import base64
import random
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = "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"

MODEL_ID = "google/gemini-3-pro-image-preview"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

INPUT_DIR = "D:\PyCharm Projects\BlueSkyExecutions\Images\OriginalImages"
OUTPUT_DIR = "D:\PyCharm Projects\BlueSkyExecutions\Text+Image\AnswerDisturbingImages"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def save_base64_image(b64_data, filepath):
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(b64_data))


def call_gemini_vision(image_path, prompt, output_path):

    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found")

    b64_image = encode_image(image_path)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mathverse-noise-injector.com",
        "X-Title": "MathVerse Noise Injector"
    }

    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "You are a specialized image augmentation assistant for a math dataset. "
                            "Recreate the provided geometry diagram while applying the requested modification. "
                            "CRITICAL: Unless explicitly instructed, preserve all numbers, labels, and geometry exactly. "
                            f"Task: {prompt}"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{b64_image}"
                        }
                    }
                ]
            }
        ],
        "modalities": ["image", "text"]
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    result = response.json()

    try:
        image_url = result["choices"][0]["message"]["images"][0]["image_url"]["url"]
        save_base64_image(image_url, output_path)
        print(f"Saved: {output_path}")

    except Exception:
        print("Error: Image not found in API response")
        print(result)


# -------------------------------------------------
# Occlusion augmentation
# -------------------------------------------------

def occlude_critical_info(image_path, output_path):

    occlusions = [
        "Overlay a large messy black ink blot that completely covers one of the numbers or variables in the diagram.",
        "Show a human finger pointing at the diagram but positioned such that it blocks the view of a critical angle or side length.",
        "Simulate a rip or tear in the paper that removes a section containing a label."
    ]

    prompt = random.choice(occlusions)

    return call_gemini_vision(image_path, prompt, output_path)


# -------------------------------------------------
# Batch processing
# -------------------------------------------------

def process_directory():

    images = [f for f in os.listdir(INPUT_DIR)
              if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    print(f"Found {len(images)} images")

    for img in images:

        input_path = os.path.join(INPUT_DIR, img)

        output_name = f"{img}"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        print(f"Processing {img}")

        occlude_critical_info(input_path, output_path)


if __name__ == "__main__":
    process_directory()