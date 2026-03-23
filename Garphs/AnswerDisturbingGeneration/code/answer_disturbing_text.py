import random
import re
import string
import nltk
from wordfreq import zipf_frequency  

try:
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    nltk.download("wordnet", quiet=True)
from nltk.corpus import wordnet


OP_TOKENS = {
    "=", "+", "-", "*", "/", "^", "%", "(", ")", "[", "]", "{", "}",
    "<", ">", "<=", ">=", "==", "!=", "~", "≈", "$", "\\", "_{", "}^"
}


def simulate_ocr_errors(text):
    """
    Aggressively replaces 0->O, 1->I, 5->S, etc.
    """
    replacements = {'0': 'O', '1': 'I', '5': 'S', '8': 'B', '6': 'G', '9': 'g', '2': 'D', '4': 'A'}
    chars = list(text)
    for i, char in enumerate(chars):
        if char in replacements and random.random() < 0.8:
            chars[i] = replacements[char]
    return "".join(chars)

import os

INPUT_DIR = r"D:\PyCharm Projects\BlueSkyExecutions\Text\Original"
OUTPUT_DIR = r"D:\PyCharm Projects\BlueSkyExecutions\Text+Image\inputs\AnswerDisturbingText"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def perturb_text(text):
    

    perturbed = simulate_ocr_errors(text)
    return perturbed


def process_directory():

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".txt")]

    print(f"Found {len(files)} question files")

    for fname in files:

        input_path = os.path.join(INPUT_DIR, fname)
        output_path = os.path.join(OUTPUT_DIR, fname)

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        perturbed = perturb_text(text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(perturbed)

        print(f"Processed: {fname}")


if __name__ == "__main__":
    process_directory()