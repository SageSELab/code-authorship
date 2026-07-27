import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import time
import argparse
import pandas as pd
import json
from captum.attr import LayerIntegratedGradients
import os
from peft import PeftModel
from attn_backend import attn_implementation

os.makedirs('explanations', exist_ok=True)

start = time.time()
parser = argparse.ArgumentParser(description='Interpret Predictions')
parser.add_argument('--tokenizer', type=str, default="codellama/CodeLlama-7b-hf",
                    help="Tokenizer to use: a Hugging Face model ID or a local directory.")
parser.add_argument('--n_steps', type=int, default=5)
parser.add_argument('--no_of_folds', type=int, default=8)
parser.add_argument('--h_config_no', type=int, default=1)
parser.add_argument('--no_of_classes', type=int, default=198)

args = parser.parse_args()

tokenizer_name = args.tokenizer
n_steps = args.n_steps
no_of_folds = args.no_of_folds
h_config_no = args.h_config_no
no_of_classes = args.no_of_classes

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

# Set pad token if missing
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token or "[PAD]"
    tokenizer.add_special_tokens({'pad_token': tokenizer.pad_token})

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
dtype = torch.float16 if torch.cuda.is_available() else torch.float32

def perturb_input(input_tokens, salient_tokens, retain=True):
    """
    Perturb input by either removing or retaining salient tokens.
    Args:
        input_tokens: List of input tokens.
        salient_tokens: List of tokens deemed salient.
        retain: If True, retain only salient tokens; if False, remove them.
    Returns:
        Perturbed input as a string.
    """
    if retain:
        perturbed_tokens = [token for token in input_tokens if token in salient_tokens]
    else:
        perturbed_tokens = [token for token in input_tokens if token not in salient_tokens]
    return tokenizer.convert_tokens_to_string(perturbed_tokens)

def forward_func(input_ids, attention_mask):
    outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask,
        output_hidden_states=True
    )
    return outputs.logits

def predict_proba(text: str, model, tokenizer):
    """
    A custom function to get class probabilities from a given text,
    using the LoRA-adapted model.
    Returns a 1D numpy array of probabilities for each class.
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True
    ).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits  # shape: [batch_size, num_labels]
    probs = torch.softmax(logits, dim=-1).squeeze(0).cpu().numpy()
    return probs

for fold in range(0, no_of_folds):
    # Load data
    test_data_df = pd.read_csv(f'data/fold_{fold}_test.csv')
    result_df = pd.read_csv(f'results/{h_config_no}_fold_{fold}_results.csv')
    result_df['code'] = test_data_df['code']

    # Focus on correct predictions
    result_df = result_df[result_df['Actual'] == result_df['Predicted']]
    #result_df.drop_duplicates(subset=['Row_Id'], keep=False, inplace=True)
    
    # Load base model and LoRA
    base_model_path = f'./models/{h_config_no}_{fold}_model'
    base_model = AutoModelForSequenceClassification.from_pretrained(
        base_model_path,
        num_labels=no_of_classes,
        attn_implementation=attn_implementation(),
        torch_dtype=dtype
    )
    base_model.config.pad_token_id = tokenizer.pad_token_id
    
    peft_model_path = f'./models/{h_config_no}_{fold}_loramodel'
    global model
    model = PeftModel.from_pretrained(base_model, peft_model_path)
    model.to(device, dtype=dtype)
    model.eval()
    
    # Set up Captum
    layer_ig = LayerIntegratedGradients(forward_func, model.get_input_embeddings())
    
    for index, row in result_df.iterrows():
        original_author = int(row['Predicted'])
        # Skip if we already have an explanation
        explanation_path = f'./explanations/{fold}_{index}_{original_author}_{row["Row_Id"]}_important_tokens.json'
        if os.path.exists(explanation_path):
            continue

        sample_code = row['code']
        # Tokenize
        inputs = tokenizer(sample_code, return_tensors="pt").to(device)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        
        # Compute attributions
        attributions_ig = layer_ig.attribute(
            inputs=input_ids,
            baselines=torch.zeros_like(input_ids),
            additional_forward_args=attention_mask,
            n_steps=n_steps,
            target=original_author
        )
        
        # Summation across embedding dimension
        token_attributions = attributions_ig.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        tokens = tokenizer.convert_ids_to_tokens(input_ids.squeeze(0).detach().cpu().numpy())

        # Collect token-attribution pairs, sort by descending attribution
        token_attr_pairs = list(zip(tokens, token_attributions))
        token_attr_pairs.sort(key=lambda x: x[1], reverse=True)
        
        print("Tokens sorted by attribution (descending):\n")
        important_tokens = []
        for tok, score in token_attr_pairs:
            print(f"{tok:>12s} => {score:.4f}")
            if score > 0:
                important_tokens.append(tok)
        
        # Save token attributions
        with open(explanation_path, 'w') as f:
            json.dump(token_attr_pairs, f, ensure_ascii=True)
        
        # Evaluate effect of perturbations on predicted probability
        probability_original = predict_proba(sample_code, model, tokenizer)[original_author]
        score = {}
        ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9]
        
        for ratio in ratios:
            k_tokens = int(len(important_tokens) * ratio)
            # **Remove** top-k tokens
            perturb_text_remove = perturb_input(tokens, important_tokens[:k_tokens], retain=False)
            probability_perturb = predict_proba(perturb_text_remove, model, tokenizer)[original_author]
            
            # PPLCR = log(prob_original) - log(prob_perturb)
            PPLCR = np.log(probability_original) - np.log(probability_perturb)
            
            # **Retain** top-k tokens
            perturb_text_retain = perturb_input(tokens, important_tokens[:k_tokens], retain=True)
            probability_perturb_retain = predict_proba(perturb_text_retain, model, tokenizer)[original_author]
            
            # PPLA = - log(prob_perturb_retain)
            PPLA = -np.log(probability_perturb_retain)
            
            print(f"Ratio: {ratio}, PPLCR: {PPLCR}, PPLA: {PPLA}, "
                  f"OriginalProb: {probability_original}, PerturbProb: {probability_perturb}")
            
            score[f"{ratio}"] = {
                "PPLCR": float(PPLCR),
                "PPLA": float(PPLA),
                "PP": float(probability_perturb),
                "PPR": float(probability_perturb_retain),
                "OP": float(probability_original)
            }
        
        # Save metrics
        metrics_path = f'./explanations/{fold}_{index}_{original_author}_{row["Row_Id"]}_metrics.json'
        with open(metrics_path, 'w') as f:
            json.dump(score, f, indent=2)
        
        print("====================")

print("Time taken:", (time.time() - start)/60, "minutes")

