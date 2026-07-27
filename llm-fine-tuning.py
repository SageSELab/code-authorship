import torch
import random
import numpy as np
import math
import argparse
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    set_seed,
    AutoConfig,
    EarlyStoppingCallback  # <-- Add this
)
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder
import json
import os
import pandas as pd

# --------------------
# Step 1: Parse Arguments
# --------------------
parser = argparse.ArgumentParser(description="Train and optimize a Transformer model with Optuna.")
parser.add_argument("--model_path", type=str, required=True,
                    help="Path to the pre-trained model or model directory.")
parser.add_argument("--fold", type=int, required=True,
                    help="Fold number for cross-validation (e.g., 0 or 1).")
parser.add_argument("--max_context_length", type=int, default=512,
                    help="Maximum context length for tokenization.")
parser.add_argument("--seed", type=int, default=42,
                    help="Random seed for reproducibility.")
parser.add_argument("--h_config_no", type=int, required=True,
                    help="Hyperparameter configuration number.")
parser.add_argument("--early_stopping_patience", type=int, default=3,
                    help="Number of epochs with no improvement in eval_f1 before early stopping.")
parser.add_argument("--num_train_epochs", type=int, default=50,
                    help="Maximum training epochs. Early stopping usually halts well "
                         "before this; lower it only for smoke tests.")

args = parser.parse_args()

model_path = args.model_path
fold = args.fold
max_context_length = args.max_context_length
random_seed = args.seed
h_config_no = args.h_config_no
early_stopping_patience = args.early_stopping_patience

# --------------------
# Step 2: Set Random Seeds
# --------------------
set_seed(random_seed)
np.random.seed(random_seed)
random.seed(random_seed)
torch.manual_seed(random_seed)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

os.makedirs("./models", exist_ok=True)
os.makedirs("./results", exist_ok=True)
os.makedirs("./data", exist_ok=True)

TRAIN_CSV = f"../data/fold_{fold}_train.csv"
TEST_CSV  = f"../data/fold_{fold}_test.csv"

if not os.path.exists(TRAIN_CSV):
    raise FileNotFoundError(f"Training CSV not found: {TRAIN_CSV}")
if not os.path.exists(TEST_CSV):
    raise FileNotFoundError(f"Test CSV not found: {TEST_CSV}")

# --------------------
# Initialize Tokenizer / LabelEncoder
# --------------------
tokenizer_path = model_path
# Special logic for contrabert if needed
if "contrabert_c" in model_path.lower():
    tokenizer_path = "microsoft/codebert-base"
elif "contrabert_g" in model_path.lower():
    tokenizer_path = "microsoft/graphcodebert-base"

tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
# Check and assign a padding token if missing
if tokenizer.pad_token is None:
    if tokenizer.eos_token:
        tokenizer.pad_token = tokenizer.eos_token
    else:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        print("Added a new [PAD] token.")

def split_data(df):
    all_rows = []
    for index, row in df.iterrows():
        tokens = tokenizer.encode(row['code'])
        if len(tokens) <= max_context_length:
            sample_row = row.to_dict()
            sample_row['row_id'] = index
            all_rows.append(sample_row)
            continue

        chunks = np.array_split(tokens, math.ceil(len(tokens) / max_context_length))
        for chunk in chunks:
            sample_row = row.to_dict()
            sample_row['code'] = tokenizer.decode(chunk.tolist())
            sample_row['row_id'] = index
            all_rows.append(sample_row)

    df_splitted = pd.DataFrame(all_rows)
    return df_splitted

# Split the data
train_df = split_data(pd.read_csv(TRAIN_CSV))
train_df.to_csv(f'./data/fold_{fold}_train.csv', index=False)
test_df = split_data(pd.read_csv(TEST_CSV))
test_df.to_csv(f'./data/fold_{fold}_test.csv', index=False)

# --------------------
# Custom Trainer
# --------------------
class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop('labels')
        outputs = model(**inputs)
        logits = outputs.get('logits')
        loss = torch.nn.functional.cross_entropy(logits, labels)
        return (loss, outputs) if return_outputs else loss

# --------------------
# Load Dataset
# --------------------
dataset = load_dataset('csv', data_files={
    'train': f'./data/fold_{fold}_train.csv',
    'validation': f'./data/fold_{fold}_test.csv'
})

train_dataset = dataset['train']
valid_dataset = dataset['validation']

valid_dataset_id = valid_dataset['row_id']
valid_sample_id = valid_dataset['sample_id']
valid_dataset_row_author = valid_dataset['author']

duplicate_row_id_dict = {}
for index, item in enumerate(np.atleast_1d(valid_dataset_id)):
    indices = np.where(np.atleast_1d(valid_dataset_id) == item)
    duplicate_row_id_dict[index] = indices[0].tolist()

print(f"Fold {fold} loaded successfully.")

label_encoder = LabelEncoder()
label_encoder.fit(train_dataset['author'])  # 'author' is your label column
num_labels = len(label_encoder.classes_)
print(f"Number of labels: {num_labels}")

# --------------------
# Preprocess Function
# --------------------
def preprocess_function(examples):
    texts = examples['code']      # Replace 'code' with your text column name
    labels = examples['author']   # Replace 'author' with your label column name
    labels = label_encoder.transform(labels)
    encodings = tokenizer(
        texts,
        truncation=True,
        padding='max_length',
        max_length=max_context_length,
    )
    encodings['labels'] = labels
    return encodings

# --------------------
# Map Preprocessing
# --------------------
train_dataset = train_dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=train_dataset.column_names
)
valid_dataset = valid_dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=valid_dataset.column_names
)

train_dataset.set_format(type='torch')
valid_dataset.set_format(type='torch')

def get_majority_logits(logits):
    """
    Aggregates logits from duplicate row_ids by summing them
    and returning a single set of logits per unique row_id.
    """
    new_logits = []
    for index, item in enumerate(logits):
        if len(duplicate_row_id_dict[index]) == 1:
            new_logits.append(item)
            continue
        sum_logits = np.zeros(len(item))
        for i in duplicate_row_id_dict[index]:
            sum_logits += logits[i]
        new_logits.append(sum_logits)
    return np.array(new_logits)

# --------------------
# Compute Metrics
# --------------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    logits = get_majority_logits(logits)
    predictions = np.argmax(logits, axis=1)
    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average='weighted', zero_division=0
    )
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }

# --------------------
# Load Hyperparameters
# --------------------
config_df = pd.read_csv(f'../../hyperparameter_combinations.csv')
config = config_df[config_df['Configuration'] == args.h_config_no]
learning_rate = float(config['Learning_Rate'].values[0])
batch_size = int(config['Batch_Size'].values[0])

# Create Model Config
model_config = AutoConfig.from_pretrained(model_path, num_labels=num_labels)
model_config.hidden_dropout_prob = 0.05
model_config.attention_probs_dropout_prob = 0.05

# Create fresh model
final_model = AutoModelForSequenceClassification.from_pretrained(
    model_path, config=model_config
).to(device)

# --------------------
# Training Arguments
# --------------------
final_args = TrainingArguments(
    output_dir=f'./finetuned_fold_{h_config_no}_{fold}',
    num_train_epochs=args.num_train_epochs,  # Max epochs (will stop earlier if no improvement)
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    learning_rate=learning_rate,
    evaluation_strategy='epoch',       # Evaluate each epoch
    save_strategy='epoch',
    logging_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model='eval_f1',   # Metric to watch for best model
    greater_is_better=True,
    save_total_limit=2,
    seed=random_seed,
    no_cuda=(not torch.cuda.is_available()),
    fp16=torch.cuda.is_available(),
    #weight_decay=0.05,
)

# --------------------
# Instantiate the Trainer with Early Stopping
# --------------------
final_trainer = CustomTrainer(
    model=final_model,
    args=final_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
    callbacks=[
        EarlyStoppingCallback(
            early_stopping_patience=early_stopping_patience,  # Stop if no improvement in eval_f1
            early_stopping_threshold=0.0                      # Threshold for "significant" improvements
        )
    ]
)

# --------------------
# Final Training
# --------------------
final_trainer.train()

# --------------------
# Evaluate
# --------------------
eval_results = final_trainer.evaluate()
print(f"Final evaluation: {eval_results}")

with open(f'./results/{h_config_no}_fold_{fold}_eval_results.json', 'w') as eval_results_file:
    json.dump(eval_results, eval_results_file, indent=4)

# --------------------
# Generate and Save Predictions
# --------------------
validation_prediction = final_trainer.predict(valid_dataset)
results_tp_fp = {
    "Actual": validation_prediction.label_ids.tolist(),
    "Predicted": np.argmax(get_majority_logits(validation_prediction.predictions), axis=1).tolist(),
    "Row_Id": valid_dataset_id,
    "Labels": valid_dataset_row_author,
    "Id": valid_sample_id
}

np.save(f"./results/{h_config_no}_fold_{fold}_validation_predictions.npy", validation_prediction.predictions)
np.save(f"./results/{h_config_no}_fold_{fold}_validation_labels.npy", validation_prediction.label_ids)
with open(f"./results/{h_config_no}_fold_{fold}_validation_chunks.json", "w") as results_file:
    json.dump(duplicate_row_id_dict, results_file, indent=4)

results_df = pd.DataFrame.from_dict(results_tp_fp)
results_df.to_csv(f"./results/{h_config_no}_fold_{fold}_results.csv", index=False)

# --------------------
# Save Final Model
# --------------------
final_trainer.save_model(f'./models/{h_config_no}_{fold}_model')
print("Model and tokenizer saved successfully.")

