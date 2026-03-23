import os
import json
import random
import re
import shutil
from datasets import load_dataset
from tqdm import tqdm

import text_noise_injection as text_noise
import image_noise_injection as image_noise


OUTPUT_DIR1 = "noisy_dataset_pg"
IMAGES_DIR1 = os.path.join(OUTPUT_DIR1, "images")
ORIGINAL_IMAGES_DIR1 = os.path.join(OUTPUT_DIR1, "original_images")
JSONL_PATH1 = os.path.join(OUTPUT_DIR1, "metadata.jsonl")
os.makedirs(IMAGES_DIR1, exist_ok=True)
os.makedirs(ORIGINAL_IMAGES_DIR1, exist_ok=True)

OUTPUT_DIR2 = "noisy_dataset_sg"
IMAGES_DIR2 = os.path.join(OUTPUT_DIR2, "images")
ORIGINAL_IMAGES_DIR2 = os.path.join(OUTPUT_DIR2, "original_images")
JSONL_PATH2 = os.path.join(OUTPUT_DIR2, "metadata.jsonl")
os.makedirs(IMAGES_DIR2, exist_ok=True)
os.makedirs(ORIGINAL_IMAGES_DIR2, exist_ok=True)

OUTPUT_DIR3 = "noisy_dataset_graph"
IMAGES_DIR3 = os.path.join(OUTPUT_DIR3, "images")
ORIGINAL_IMAGES_DIR3 = os.path.join(OUTPUT_DIR3, "original_images")
JSONL_PATH3 = os.path.join(OUTPUT_DIR3, "metadata.jsonl")
os.makedirs(IMAGES_DIR3, exist_ok=True)
os.makedirs(ORIGINAL_IMAGES_DIR3, exist_ok=True)


problem_idxs_plane_geometry = list(map(str, [14, 52, 64, 84, 95, 99, 107, 108, 115, 120, 132, 136, 151, 152, 153, 157, 223, 257, 264, 281, 298, 364, 365, 438, 441, 447, 449, 457, 472, 779])) 
problem_idxs_solid_geometry = list(map(str, [650, 670, 676, 678, 716, 731, 732, 740, 742, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 651, 652, 653, 654, 655, 656]))
problem_idxs_graph = list(map(str, [476, 481, 486, 492, 497, 503, 567, 568, 582, 588, 623, 474, 475, 477, 478, 479, 480, 482, 483, 484, 485, 487, 488, 489, 490, 491, 493, 494, 495, 496]))


TEXT_CAT_1 = [
    ("inject_typos", text_noise.inject_typos),
    ("add_distractor_sentences", text_noise.add_distractor_sentences),
    ("swap_punctuation", text_noise.swap_punctuation),
    ("add_numeric_distractors", text_noise.add_numeric_distractors)
]

TEXT_CAT_2 = [
    ("simulate_ocr_errors", text_noise.simulate_ocr_errors),
    ("modify_geometric_values", text_noise.modify_geometric_values),
    ("remove_geometric_properties", text_noise.remove_geometric_properties)
]

IMAGE_CAT_1 = [
    ("change_background", image_noise.change_background),
    ("simulate_uneven_illumination", image_noise.simulate_uneven_illumination),
    ("insert_irrelevant_objects", image_noise.insert_irrelevant_objects),
    ("make_disproportionate", image_noise.make_disproportionate)
]

IMAGE_CAT_2 = [
    ("modify_image_values", image_noise.modify_image_values),
    ("occlude_critical_info", image_noise.occlude_critical_info)
]

def convert_to_free_form(text):
    if not text:
        return text
    text = re.sub(r'\s*\(\s*\)\s*Choices:.*', '', text, flags=re.DOTALL)
    text = re.sub(r'\s*Choices:.*', '', text, flags=re.DOTALL)
    return text.strip()

def get_filtered_samples(target_idxs_list, ds_main, ds_text):
    target_idxs = set(str(x) for x in target_idxs_list) if target_idxs_list else None
    
    text_samples = {}
    for sample in ds_text:
        pid = str(sample["problem_index"])
        if target_idxs is not None and pid not in target_idxs: continue
        text_samples[pid] = sample

    vision_samples = {}
    for sample in ds_main:
        pid = str(sample["problem_index"])
        version = sample["problem_version"]
        if target_idxs is not None and pid not in target_idxs: continue
        if version == "Vision Only":
            vision_samples[pid] = sample

    for pid in text_samples.keys():
        if pid in vision_samples:
            yield text_samples[pid], "Text Only"
            yield vision_samples[pid], "Vision Only"
            
            combined_sample = text_samples[pid].copy()
            combined_sample["image"] = vision_samples[pid]["image"]
            yield combined_sample, "Text + Image"

def apply_text_noise(text, category_strategies):
    if not text: return text, []
    
    noisy_texts = {}
    applied = []
    
    for name, func in category_strategies:
        try:
            res = func(text)
            noisy_texts[name] = res
            applied.append(name)
        except Exception:
            pass
            
    return noisy_texts, applied

def apply_image_noise(image_input, pid, version, category_strategies, images_dir):
    if not image_input: return [], []
    
    temp_input = os.path.join(images_dir, f"temp_{pid}_in.png")
    
    if isinstance(image_input, str):
        shutil.copy(image_input, temp_input)
    else:
        image_input.save(temp_input)
    
    paths = []
    applied = []
    
    for name, func in category_strategies:
        final_name = f"{pid}_{version.replace(' ','')}_{name}.png"
        output_path = os.path.join(images_dir, final_name)
        
        success = False
        while not success:
            success = func(temp_input, output_path)
            if not success:
                print(f"Retrying image generation '{name}' for problem {pid}...")
        
        paths.append(output_path)
        applied.append(name)

    if os.path.exists(temp_input):
        os.remove(temp_input)
        
    return paths, applied

def process_category(target_idxs, images_dir, orig_images_dir, jsonl_path, ds_main, ds_text):
    samples = list(get_filtered_samples(target_idxs, ds_main, ds_text))
    if len(samples) == 0: return

    with open(jsonl_path, "w", encoding="utf-8") as f_out:
        for sample, version in tqdm(samples, desc=f"Processing {os.path.basename(jsonl_path)}"):
            while True:
                try:
                    pid = str(sample["problem_index"])
                    raw_ans = sample.get("answer", "")
                    original_question = convert_to_free_form(sample["question"])
                    image = sample["image"]
                    q_type = sample.get("question_type", "")
                    
                    orig_img_path = ""
                    if image:
                        orig_img_name = f"{pid}_{version.replace(' ','')}_original.png"
                        orig_img_path = os.path.join(orig_images_dir, orig_img_name)
                        
                        if isinstance(image, str):
                            shutil.copy(image, orig_img_path)
                        else:
                            image.save(orig_img_path)
                            
                        if q_type == "multi-choice":
                            temp_mcq_in = os.path.join(orig_images_dir, f"temp_{pid}_mcq_in.png")
                            shutil.move(orig_img_path, temp_mcq_in)
                            
                            mcq_success = False
                            while not mcq_success:
                                mcq_success = image_noise.remove_mcq_choices(temp_mcq_in, orig_img_path)
                                if not mcq_success:
                                    print(f"Retrying MCQ removal for original image {pid}...")
                            
                            if os.path.exists(temp_mcq_in):
                                os.remove(temp_mcq_in)
                        
                        image = orig_img_path
                    
                    record = {
                        "problem_index": pid,
                        "version": version,
                        "original_question": original_question,
                        "original_image_path": orig_img_path,
                        "ground_truth_answer": raw_ans,
                        "noisy_question": "",
                        "noisy_image_paths": [],
                        "applied_text_noise": [],
                        "applied_image_noise": []
                    }
                    
                    if version == "Text Only":
                        nq, t_mods = apply_text_noise(original_question, TEXT_CAT_1)
                        record["noisy_question"] = nq
                        record["applied_text_noise"] = t_mods
                        
                    elif version == "Vision Only":
                        record["noisy_question"] = original_question
                        
                        paths, i_mods = apply_image_noise(image, pid, version, IMAGE_CAT_1, images_dir)
                        record["noisy_image_paths"] = paths
                        record["applied_image_noise"] = i_mods
                        
                    elif version == "Text + Image":
                        nq, t_mods = apply_text_noise(original_question, TEXT_CAT_2)
                        paths, i_mods = apply_image_noise(image, pid, version, IMAGE_CAT_2, images_dir)
                        
                        record["noisy_question"] = nq
                        record["noisy_image_paths"] = paths
                        record["applied_text_noise"] = t_mods
                        record["applied_image_noise"] = i_mods

                    f_out.write(json.dumps(record) + "\n")
                    f_out.flush()
                    break
                except Exception as e:
                    print(f"Error processing {pid}: {e}")
                    pass

def main():
    print("Loading MathVerse dataset...")
    ds_main = load_dataset("AI4Math/MathVerse", "testmini", split="testmini")
    ds_text = load_dataset("AI4Math/MathVerse", "testmini_text_only", split="testmini_text_only")

    configs = [
        ("Plane Geometry", problem_idxs_plane_geometry, IMAGES_DIR1, ORIGINAL_IMAGES_DIR1, JSONL_PATH1),
        ("Solid Geometry", problem_idxs_solid_geometry, IMAGES_DIR2, ORIGINAL_IMAGES_DIR2, JSONL_PATH2),
        ("Graphs", problem_idxs_graph, IMAGES_DIR3, ORIGINAL_IMAGES_DIR3, JSONL_PATH3)
    ]

    for name, target_idxs, images_dir, orig_images_dir, jsonl_path in configs:
        print(f"\n--- Starting Processing for {name} ---")
        process_category(target_idxs, images_dir, orig_images_dir, jsonl_path, ds_main, ds_text)

if __name__ == "__main__":
    main()