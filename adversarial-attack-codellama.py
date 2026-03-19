import os
import pandas as pd
import numpy as np
import argparse
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import math
from tqdm import tqdm
from peft import PeftModel

# Reduce memory fragmentation
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64"
torch.cuda.empty_cache()

parser = argparse.ArgumentParser(description="Adversarial Attack on CodeLlama")

parser.add_argument("--tokenizer_path", type=str, required=True, help="Path to the tokenizer directory")
parser.add_argument("--h_config", type=str, required=True, help="Path to the hyperparameter config file no.")
parser.add_argument("--model_name", type=str, required=True, help="Name of the model for the attack")
parser.add_argument("--max_context_length", type=int, default=2233, help="Maximum context length for tokenization.")
parser.add_argument("--no_of_classes", type=int, default=198, help="Number of classes for the model.")

args = parser.parse_args()
tokenizer_path = args.tokenizer_path
h_config = args.h_config
model_name = args.model_name
max_context_length = args.max_context_length
no_of_classes = args.no_of_classes

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# Set pad token if missing
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token or "[PAD]"
    tokenizer.add_special_tokens({'pad_token': tokenizer.pad_token})

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

df = pd.read_csv("../../adversarial_samples_GPT4_accepted.csv")
df = df[df[f"{model_name}"] == True]

# Separate caches for models and results
results_cache = {}
#model_cache = {}

dtype = torch.float16 if torch.cuda.is_available() else torch.float32

def get_actual_class(fold_no, sample_no):
    key = (h_config, fold_no)
    if key not in results_cache:
        results_cache[key] = pd.read_csv(f"./results/{h_config}_fold_{fold_no}_results.csv")
    result_df = results_cache[key]
    result_df = result_df[result_df["Id"] == int(sample_no)]
    return result_df["Predicted"].values[0]

def split_data(code):
    tokens = tokenizer.encode(code)
    if len(tokens) <= max_context_length:
        return [code]
    chunks = np.array_split(tokens, math.ceil(len(tokens) / max_context_length))
    return [tokenizer.decode(chunk.tolist()) for chunk in chunks]

df['fold_no'] = df['location'].apply(lambda x: x.split("_")[1])

df_grouped = df.groupby('fold_no')

for fold_no, group in df_grouped:
    base_model = AutoModelForSequenceClassification.from_pretrained(f'./models/{h_config}_{fold_no}_model', num_labels=no_of_classes, attn_implementation="flash_attention_2", torch_dtype=dtype)
    if tokenizer.pad_token == '[PAD]':
        base_model.resize_token_embeddings(len(tokenizer))
    
    base_model.config.pad_token_id = tokenizer.pad_token_id
    peft_model_path = f'./models/{h_config}_{fold_no}_loramodel'  # directory containing LoRA adapters
    model = PeftModel.from_pretrained(base_model, peft_model_path)
    model.to(device, dtype=dtype)
    model.eval()
    
    for index, row in tqdm(group.iterrows(), total=len(group), desc=f"Processing Fold {fold_no}"):
        code = row["adversarial_code"]
        all_rows = split_data(code)
        probabilities = np.zeros(no_of_classes)
        for code_chunk in all_rows:
            inputs = tokenizer(code_chunk, return_tensors="pt", padding='max_length', max_length=max_context_length, truncation=True).to(device)
            with torch.no_grad():
                logits = model(**inputs).logits
                probs = torch.nn.functional.softmax(logits, dim=-1).cpu().numpy()
                probabilities += probs.squeeze(0)
            del inputs, logits, probs
            torch.cuda.empty_cache()
        predicted_class = np.argmax(probabilities)
        confidence = probabilities[predicted_class]
        df.loc[index, ["predicted_class", "confidence"]] = [predicted_class, confidence
        ]
        actual_class = get_actual_class(fold_no, row["location"].split("_")[2])
        df.loc[index, ["actual_class", "correct"]] = [actual_class, predicted_class == actual_class]
        print(f"Sample {row['location'].split('_')[2]} | Fold {fold_no} | Pred: {predicted_class} | Actual: {actual_class} | Correct: {predicted_class == actual_class} | Confidence: {confidence:.4f}")
    del model
# Save results
df.to_csv(f"./results/adversarial_samples_GPT4_accepted_{model_name}_predictions.csv", index=False)
    
