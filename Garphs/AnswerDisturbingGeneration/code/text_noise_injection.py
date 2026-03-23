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

def split_trailing_punct(tok: str):
    """Separates word from trailing punctuation (keeping decimals in numbers)."""
    m = re.fullmatch(r"(.*?)([.,!?;:]*)", tok)
    return (m.group(1), m.group(2)) if m else (tok, "")

def is_operator(tok: str) -> bool:
    core, _ = split_trailing_punct(tok)
    return core in OP_TOKENS or any(op in tok for op in OP_TOKENS)

def is_number_token(tok: str) -> bool:
    """Checks for numbers, including decimals (27.5) and commas (27,000)."""
    core, _ = split_trailing_punct(tok)
    
    return bool(re.fullmatch(r"\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?", core))

def contains_digit(tok: str) -> bool:
    return bool(re.search(r"\d", tok))

def protected_indices(tokens: list) -> set:
    """
    Returns indices of tokens that should NOT be modified (math, numbers, operators).
    Protects the token itself and its immediate neighbors to preserve context.
    """
    bad = set()
    n = len(tokens)
    for i, tok in enumerate(tokens):
        if is_number_token(tok) or contains_digit(tok) or is_operator(tok):
            for j in (i - 1, i, i + 1):
                if 0 <= j < n:
                    bad.add(j)
    return bad

def extract_numbers(text: str) -> set:
    return set(re.findall(r"\d+", text))

def sentence_boundaries(text: str) -> list:
    """Finds safe insertion points for sentences (avoiding decimals)."""
    boundaries = []
    for i, ch in enumerate(text):
        if ch not in ".!?": continue
        prev_ch = text[i - 1] if i > 0 else ""
        next_ch = text[i + 1] if i + 1 < len(text) else ""
        # Avoid splitting 3.14
        if prev_ch.isdigit() and next_ch.isdigit(): continue
        boundaries.append(i + 1)
    return boundaries if boundaries else [len(text)]


### CATEGORY 1: No major loss of relevant information (Problem is still solvable with this modality alone)


def inject_typos(text, error_rate=0.2):
    """
    Randomly drops or swaps characters in NON-MATH words.
    """
    tokens = text.split()
    bad = protected_indices(tokens)
    
    # Identify editable indices
    editable = []
    for i, t in enumerate(tokens):
        if i in bad: continue
        core, punct = split_trailing_punct(t)
        if len(core) >= 4 and core.isalpha():
            editable.append((i, core, punct))
            
    # Apply typos
    num_errors = max(1, int(len(editable) * error_rate))
    for _ in range(num_errors):
        if not editable: break
        idx_in_editable = random.randrange(len(editable))
        i, core, punct = editable.pop(idx_in_editable)
        
        # 50/50 swap or drop
        if random.random() < 0.5: # Drop
            char_idx = random.randrange(len(core))
            new_core = core[:char_idx] + core[char_idx+1:]
        else: # Swap
            char_idx = random.randrange(len(core) - 1)
            new_core = core[:char_idx] + core[char_idx+1] + core[char_idx] + core[char_idx+2:]
            
        tokens[i] = new_core + punct
        
    return " ".join(tokens)

def add_distractor_sentences(text):
    """
    Inserts irrelevant sentences at valid sentence boundaries.
    """
    distractors = [
        "It was sunny today.", "The teacher wrote this on the board.",
        "Make sure to show your work.", "John was thinking about lunch.",
        "The diagram is drawn to scale.", "Please turn to page 42.",
        "I lost my geometry box yesterday.", "The library closes early."
    ]
    
    # Try to insert 1 or 2 distractors
    k = random.randint(1, 2)
    boundaries = sentence_boundaries(text)
    existing_nums = extract_numbers(text)
    
    current_text = text
    for _ in range(k):
        sent = random.choice(distractors)
        # Don't add distractors that contain numbers present in the problem
        if extract_numbers(sent) & existing_nums: continue
            
        if not boundaries: break
        
        pos = random.choice(boundaries)
        current_text = current_text[:pos] + " " + sent + " " + current_text[pos:]
        boundaries = sentence_boundaries(current_text) # Recompute
        
    return current_text

def swap_punctuation(text):
    """
    Swaps '.' with ',' and vice versa, BUT protects numbers (decimals/coords).
    """
    tokens = text.split()
    bad = protected_indices(tokens) # This protects numbers like 3.14
    
    new_tokens = []
    for i, tok in enumerate(tokens):
        if i in bad:
            new_tokens.append(tok)
        else:
            # Safe to swap punctuation in this token
            trans_table = str.maketrans({'.': ',', ',': '.'})
            new_tokens.append(tok.translate(trans_table))
            
    return " ".join(new_tokens)

def add_numeric_distractors(text):
    """
    Adds irrelevant numbers (like years, page numbers) in SAFE slots.
    """
    tokens = text.split()
    existing_nums = extract_numbers(text)
    
    # Generate a candidate number that doesn't exist in the problem
    candidate = str(random.randint(10, 2025))
    while candidate in existing_nums:
        candidate = str(random.randint(10, 2025))
        
    distractor_phrases = [
        f"(Ref: {candidate})", f"[Page {candidate}]", f"ID:{candidate}"
    ]
    
    chosen = random.choice(distractor_phrases)
    bad = protected_indices(tokens)
    
    # Find safe slots (not next to math)
    safe_slots = []
    for slot in range(len(tokens) + 1):
        left = slot - 1
        right = slot
        if (left >= 0 and left in bad) or (right < len(tokens) and right in bad):
            continue
        safe_slots.append(slot)
        
    if safe_slots:
        slot = random.choice(safe_slots)
        tokens.insert(slot, chosen)
        
    return " ".join(tokens)


### CATEGORY 2: Loss of relevant information (VLM is forced to look at other modality)


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

def modify_geometric_values(text):
    """
    Changes integers to different values, violating constraints.
    """
    def replace_num(match):
        val = int(match.group())
        # Change value by +/- small amount, ensure > 0
        new_val = max(1, val + random.choice([-2, -1, 1, 2, 3]))
        return str(new_val)

    # Regex to find standalone integers (excludes floats for simplicity)
    # Lookbehind ensures we aren't inside a LaTeX command like \frac{1}
    return re.sub(r'(?<![\\{}])\b\d+\b', replace_num, text)

def remove_geometric_properties(text):
    """
    Removes keywords like 'right-angled', 'isosceles', 'parallel'.
    """
    keywords = [
        r"\bright-angled\b", r"\bright angle\b", r"\bisosceles\b", 
        r"\bequilateral\b", r"\bparallel\b", r"\bperpendicular\b"
    ]
    current_text = text
    for kw in keywords:
        current_text = re.sub(kw, "", current_text, flags=re.IGNORECASE)
    
    # Cleanup double spaces
    return re.sub(r'\s+', ' ', current_text).strip()