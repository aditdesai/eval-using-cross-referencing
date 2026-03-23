import os
import json
import base64
import random
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_ID = "google/gemini-3-pro-image-preview"
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def encode_image(image_path):
    """Encodes a local image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def save_base64_image(b64_data, filepath):
    if "," in b64_data:
        b64_data = b64_data.split(",", 1)[1]
    
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(b64_data))

def call_gemini_vision(image_input, prompt, filename):
    """
    Sends an image + prompt to Gemini via OpenRouter.
    image_input: Can be a file path (str) or raw bytes.
    """
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    if os.path.isfile(image_input):
        b64_image = encode_image(image_input)
    else:
        b64_image = image_input

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
                            "Your task is to take the provided geometry diagram and RECREATE it "
                            "while applying a specific visual modification. "
                            "CRITICAL: Unless explicitly told to change values, you MUST preserve "
                            "all original numbers, variable labels, and geometric structures exactly. "
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

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()


        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0]["message"]
            
            if "images" in message and len(message["images"]) > 0:
                image_url = message["images"][0]["image_url"]["url"]
                save_base64_image(image_url, filename)
                print(f"   -> Saved to {filename}")

                return True
            else:
                print(f"   [Error] No image found in response: {result}")
            
        print("Warning: No image found in response.")
        return None

    except Exception as e:
        print(f"API Request Failed: {e}")
        return None


def remove_mcq_choices(image_path, filename):
    prompt = (
        "This image contains a math question text at the top and a geometry diagram. "
        "The question is multiple-choice and contains the word 'Choices:' followed by options (A, B, C, D). "
        "Please recreate this image perfectly, preserving the diagram and the main question text, "
        "but COMPLETELY REMOVE the 'Choices:' section and all the options. Leave that area blank "
        "so the question appears as a free-form question."
    )
    return call_gemini_vision(image_path, prompt, filename)


### CATEGORY 1: No major loss of relevant information (Problem is still solvable with this modality alone)

def change_background(image_path, filename):
    """
    Simulates different paper textures (Graph, Crumpled, Blackboard).
    """
    strategies = [
        "Draw this diagram on a sheet of graph paper (grid background). Keep lines dark and distinct.",
        "Draw this diagram on a piece of crumbled, wrinkled white paper.",
        "Draw this diagram as if it were drawn with white chalk on a dark green blackboard."
    ]
    selected_prompt = random.choice(strategies)
    return call_gemini_vision(image_path, selected_prompt, filename)

def simulate_uneven_illumination(image_path, filename):
    """
    Adds shadows or uneven lighting.
    """
    prompt = (
        "Recreate this diagram exactly, but simulate uneven lighting. "
        "Cast a realistic, soft shadow across the top-right corner of the image, "
        "as if a hand or object is blocking the light. Ensure the diagram remains legible underneath."
    )
    return call_gemini_vision(image_path, prompt, filename)

def insert_irrelevant_objects(image_path, filename):
    """
    Inserts objects like coffee stains or pencils.
    """
    objects = [
        "Place a realistic circular coffee mug stain on the paper, slightly overlapping a non-critical part of the diagram.",
        "Place a yellow wooden pencil lying diagonally across the empty space of the paper.",
        "Show a paperclip resting on the side of the diagram."
    ]
    selected_prompt = random.choice(objects)
    return call_gemini_vision(image_path, selected_prompt, filename)

def make_disproportionate(image_path, filename):
    """
    Warps the aspect ratio/scale without changing labels.
    """
    prompt = (
        "Redraw this geometry diagram but distort the visual proportions. "
        "Stretch the shapes horizontally or vertically so that they look visually "
        "disproportionate to their labels (e.g., a square looking like a rectangle). "
        "CRITICAL: Keep the text labels and numbers EXACTLY as they are in the original."
    )
    return call_gemini_vision(image_path, prompt, filename)


### CATEGORY 2: Loss of relevant information (VLM is forced to look at other modality)


def modify_image_values(image_path, filename):
    """
    Changes numerical values (labels) in the image to violate constraints.
    """
    prompt = (
        "Recreate this diagram, but I want you to CHANGE one of the numerical labels "
        "to a value that makes no geometric sense. "
        "For example, if there is a right angle, label it '100°', or if two sides look equal, "
        "label one '5' and the other '20'. Only change the text label; keep the drawing the same."
    )
    return call_gemini_vision(image_path, prompt, filename)

def occlude_critical_info(image_path, filename):
    """
    Occludes critical parts of the diagram (Ink blot, Hand, Tear).
    """
    occlusions = [
        "Overlay a large, messy black ink blot that completely covers one of the numbers or variables in the diagram.",
        "Show a human finger pointing at the diagram, but positioned such that it blocks the view of a critical angle or side length.",
        "Simulate a rip or tear in the paper that removes a section of the diagram containing a label."
    ]
    selected_prompt = random.choice(occlusions)
    return call_gemini_vision(image_path, selected_prompt, filename)