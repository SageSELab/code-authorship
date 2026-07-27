import pandas as pd
import numpy as np
import argparse
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import math
from tqdm import tqdm

import sys as _sys
from pathlib import Path as _Path

# Run from data/{dataset}/{model}/; reach the shared helpers via src/.
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from common.paths import REPO_ROOT


parser = argparse.ArgumentParser(description="Adversarial Attack on CodeBERT")

parser.add_argument("--tokenizer_path", type=str, required=True, help="Path to the tokenizer directory")
parser.add_argument("--h_config", type=str, required=True, help="Path to the hyperparameter config file no.")
parser.add_argument("--model_name", type=str, required=True, help="Name of the model for the attack")
parser.add_argument("--max_context_length", type=int, default=512, help="Maximum context length for tokenization.")
parser.add_argument("--no_of_classes", type=int, default=198, help="Number of classes for the model.")

args = parser.parse_args()
tokenizer_path = args.tokenizer_path
h_config = args.h_config
model_name = args.model_name
max_context_length = args.max_context_length
no_of_classes = args.no_of_classes

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df = pd.read_csv(REPO_ROOT / "adversarial_samples_GPT4_accepted.csv")
df = df[df[f"{model_name}"] == True]

# Separate caches for models and results
results_cache = {}
model_cache = {}

def get_actual_class(fold_no, sample_no):
    key = (h_config, fold_no)
    if key not in results_cache:
        results_cache[key] = pd.read_csv(f"./results/{h_config}_fold_{fold_no}_results.csv")
    result_df = results_cache[key]
    result_df = result_df[result_df["Id"] == int(sample_no)]
    
    return result_df["Predicted"].values[0]

def split_data(code):
    """Split long code sequences into chunks respecting max context length."""
    tokens = tokenizer.encode(code)
    if len(tokens) <= max_context_length:
        return [code]
    chunks = np.array_split(tokens, math.ceil(len(tokens) / max_context_length))
    return [tokenizer.decode(chunk.tolist()) for chunk in chunks]

# Process adversarial samples
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing Samples"):
    code = row["adversarial_code"]
    all_rows = split_data(code)
    _, fold_no, sample_no = row["location"].split("_")

    # Load model once per fold
    model_key = (h_config, fold_no)
    if model_key not in model_cache:
        model = AutoModelForSequenceClassification.from_pretrained(f'./models/{h_config}_{fold_no}_model', num_labels=no_of_classes).to(device)
        model.eval()
        model_cache[model_key] = model
    else:
        model = model_cache[model_key]

    # Process tokenized chunks
    probabilities = np.zeros(no_of_classes)
    for code_chunk in all_rows:
        inputs = tokenizer(code_chunk, return_tensors="pt", padding=True, truncation=True, max_length=max_context_length).to(device)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=-1).cpu().numpy()
            probabilities += probs.squeeze(0)

    predicted_class = np.argmax(probabilities)
    confidence = probabilities[predicted_class]

    # Store results
    df.loc[index, ["predicted_class", "confidence"]] = [predicted_class, confidence]
    actual_class = get_actual_class(fold_no, sample_no)
    df.loc[index, ["actual_class", "correct"]] = [actual_class, predicted_class == actual_class]

    print(f"Sample {sample_no} | Fold {fold_no} | Pred: {predicted_class} | Actual: {actual_class} | Correct: {predicted_class == actual_class} | Confidence: {confidence:.4f}")

# Save results
df.to_csv(f"./results/adversarial_samples_GPT4_accepted_{model_name}_predictions.csv", index=False)
