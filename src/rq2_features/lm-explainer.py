
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import transformers
import time
import argparse
import pandas as pd
import json
from captum.attr import IntegratedGradients, LayerIntegratedGradients
import os

os.makedirs('explanations', exist_ok=True)

start = time.time()
parser = argparse.ArgumentParser(description='Interpret Predictions')
parser.add_argument('--tokenizer', type=str, default="")
parser.add_argument('--n_steps', type=int, default=200)
parser.add_argument('--no_of_folds', type=int, default=200)
parser.add_argument('--h_config_no', type=int, required=True)

args = parser.parse_args()

tokenizer_name = args.tokenizer
n_steps = args.n_steps
no_of_folds = args.no_of_folds
h_config_no = args.h_config_no

# Load pre-trained BERT model and tokenizer
tokenizer_name = tokenizer_name  # Change this to your fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def perturb_input(input_tokens, salient_tokens, retain=True):
            """
            Perturb input by either removing or retaining salient tokens.
            Args:
                input_tokens: List of input tokens.
                salient_tokens: List of tokens deemed salient.
                retain: If True, retain only salient tokens; if False, remove salient tokens.
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

ig = IntegratedGradients(forward_func)

for fold in range(0, no_of_folds):
    test_data_df = pd.read_csv(f'data/fold_{fold}_test.csv')
    result_df = pd.read_csv(f'results/{h_config_no}_fold_{fold}_results.csv')
    result_df['code'] = test_data_df['code']

    # Focus on correct predictions
    result_df = result_df[result_df['Actual'] == result_df['Predicted']]
    
    result_df.drop_duplicates(subset=['Row_Id'],keep=False, inplace=True)
    
    model = AutoModelForSequenceClassification.from_pretrained(f"./models/{h_config_no}_{fold}_model")
    model.eval()
    
    layer_ig = LayerIntegratedGradients(forward_func, model.get_input_embeddings())
    
    for index, row in result_df.iterrows():
        original_author = int(row['Predicted'])
        if os.path.exists(f'./explanations/{fold}_{index}_{original_author}_{row["Row_Id"]}_important_tokens.json'):
            continue
        pred = transformers.pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            device=device,
            return_all_scores=True)
    
        sample_code = row['code']
        original_author = int(row['Predicted'])
        inputs = tokenizer(sample_code, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)
        
        attributions_ig = layer_ig.attribute(
            inputs=input_ids,
            baselines=(torch.zeros_like(input_ids),),
            additional_forward_args=attention_mask,
            n_steps=n_steps,
            target=original_author
        )
        
        token_attributions = attributions_ig.sum(dim=-1).squeeze(0).detach().cpu().numpy()
        tokens = tokenizer.convert_ids_to_tokens(input_ids.squeeze(0).detach().cpu().numpy())

        # Collect token-attribution pairs
        token_attr_pairs = list(zip(tokens, token_attributions))

        # ------------------------
        #  Option A: Sort by raw values descending
        # ------------------------
        token_attr_pairs.sort(key=lambda x: x[1], reverse=True)
        
        print("Tokens sorted by attribution (descending):\n")
        important_tokens = []
        for tok, score in token_attr_pairs:
            print(f"{tok:>12s} => {score:.4f}")
            #if score> 0:
            important_tokens.append(tok)
        
        
        with open(f'./explanations/{fold}_{index}_{original_author}_{row["Row_Id"]}_important_tokens.json', 'w') as f:
            json.dump(token_attr_pairs, f, ensure_ascii=True)
        
        

        ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9]
        probability_original = pred(sample_code)[0][original_author]['score']
        score = {}
        for ratio in ratios:
            # Perturb input by removing salient tokens
            k_tokens = int(len(tokens) * ratio)
            
            # PPLCR
            perturb_input_tokens = perturb_input(tokens, important_tokens[:k_tokens], retain=False)
            probability_perturb = pred(perturb_input_tokens)[0][original_author]['score']
            PPLCR = np.log(probability_original) - np.log(probability_perturb)
            
            # PPLA
            perturbed_input_retain_tokens = perturb_input(tokens, important_tokens[:k_tokens], retain=True)
            probability_perturb_retain = pred(perturbed_input_retain_tokens)[0][original_author]['score']
            PPLA = - np.log(probability_perturb_retain)
            
            print(f"Ratio: {ratio}, PPLCR: {PPLCR}, PPLA: {PPLA} , Orignal: {probability_original}, Probability Perturb: {probability_perturb}")
            
            score[f"{ratio}"] = {"PPLCR": PPLCR, "PPLA": PPLA, "PP": probability_perturb, "PPR": probability_perturb_retain}
        
        with open(f'./explanations/{fold}_{index}_{original_author}_{row["Row_Id"]}_metrics.json', 'w') as f:
            json.dump(score, f)
        



