import torch
import random
import numpy as np
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    set_seed
)
from datasets import load_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.preprocessing import LabelEncoder
import sys
import json
import os
import pandas as pd
import optuna
from optuna.samplers import TPESampler
import optuna.visualization as vis

# --------------------
# Step 1: Import / Setup
# --------------------
random_seed = 42
set_seed(random_seed)
np.random.seed(random_seed)
random.seed(random_seed)
torch.manual_seed(random_seed)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

model_path = sys.argv[1]    # e.g., "./some_model_dir"
fold = int(sys.argv[2])     # e.g., 0 or 1
max_context_length = int(sys.argv[3])  # e.g., 512

os.makedirs("./models", exist_ok=True)
os.makedirs("./results", exist_ok=True)

TRAIN_CSV = f"../data/fold_{fold}_train.csv"
TEST_CSV  = f"../data/fold_{fold}_test.csv"

if not os.path.exists(TRAIN_CSV):
    raise FileNotFoundError(f"Training CSV not found: {TRAIN_CSV}")
if not os.path.exists(TEST_CSV):
    raise FileNotFoundError(f"Test CSV not found: {TEST_CSV}")

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
# Compute Metrics
# --------------------
def compute_metrics(eval_pred):
    logits, labels = eval_pred
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
# Helper: Add ID to examples (optional)
# --------------------
def add_id_column(example, idx):
    example['id'] = idx
    return example

# --------------------
# Load Dataset
# --------------------
dataset = load_dataset('csv', data_files={
    'train': TRAIN_CSV,
    'validation': TEST_CSV
})

train_dataset = dataset['train']
valid_dataset = dataset['validation']

# Optionally add an ID column to valid_dataset
valid_dataset = valid_dataset.map(add_id_column, with_indices=True)
valid_dataset_id = valid_dataset['id']
valid_dataset_row_author = valid_dataset['author']

print(f"Fold {fold} loaded successfully.")

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

print('Processed dataset.')

# --------------------
# Optuna Objective Function
# --------------------
def optuna_objective(trial):
    """
    The objective function for Optuna. It samples hyperparameters, creates a Trainer,
    trains, evaluates, and returns the metric to maximize (eval_accuracy).
    """

    # 1) Suggest Hyperparameters
    learning_rate = trial.suggest_float("learning_rate", 1e-6, 5e-5, log=True)
    batch_size = trial.suggest_categorical("batch_size", [8, 16, 32])
    num_train_epochs = trial.suggest_int("num_train_epochs", 5, 40, step=5)
    weight_decay = trial.suggest_float("weight_decay", 0.0, 0.1, step=0.01)

    # 2) Create Model & Training Args with these hyperparams
    temp_model = AutoModelForSequenceClassification.from_pretrained(
        model_path, num_labels=num_labels
    )

    tuning_args = TrainingArguments(
        output_dir=f'./optuna_tmp/{fold}',  # Temp directory for each trial
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        evaluation_strategy='epoch',
        save_strategy='epoch',
        logging_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model='eval_f1',
        greater_is_better=True,
        save_total_limit=1,
        seed=random_seed,
        weight_decay=weight_decay
    )

    # 3) Create Trainer
    temp_trainer = CustomTrainer(
        model=temp_model,
        args=tuning_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    # 4) Train
    temp_trainer.train()

    # 5) Evaluate
    eval_results = temp_trainer.evaluate()
    # Return the metric to maximize
    return eval_results["eval_f1"]

# --------------------
# Run Optuna Study
# --------------------
sampler = TPESampler(seed=random_seed)
study = optuna.create_study(direction="maximize", sampler=sampler)
study.optimize(optuna_objective, n_trials=10)  # Increase n_trials as needed

trials_df = study.trials_dataframe()

trials_df.to_csv(f'./results/fold_{fold}_optuna_all_trials.csv', index=False)

fig1 = vis.plot_optimization_history(study)
fig2 = vis.plot_param_importances(study)

fig1.write_image(f'./results/fold_{fold}_optuna_optimization_history.png')
fig2.write_image(f'./results/fold_{fold}_optuna_param_importances.png')

print("Best trial found:")
best_trial = study.best_trial
print(f"  Value (eval_accuracy): {best_trial.value}")
print("  Params:")
for k, v in best_trial.params.items():
    print(f"    {k}: {v}")

with open(f'./results/fold_{fold}_optuna_best_trial.json', 'w') as best_trial_file:
    json.dump(best_trial.params, best_trial_file, indent=4)

# --------------------
# Retrain with Best Hyperparams
# --------------------
best_learning_rate = best_trial.params["learning_rate"]
best_batch_size = best_trial.params["batch_size"]
best_num_train_epochs = best_trial.params["num_train_epochs"]
best_weight_decay = best_trial.params["weight_decay"]

print("\nRetraining final model with best hyperparameters...")

# Create fresh model
final_model = AutoModelForSequenceClassification.from_pretrained(
    model_path, num_labels=num_labels
)

final_args = TrainingArguments(
    output_dir=f'./finetuned_fold/{fold}',
    num_train_epochs=best_num_train_epochs,
    per_device_train_batch_size=best_batch_size,
    per_device_eval_batch_size=best_batch_size,
    learning_rate=best_learning_rate,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    logging_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model='eval_f1',
    greater_is_better=True,
    save_total_limit=2,
    seed=random_seed,
    weight_decay=best_weight_decay
)

final_trainer = CustomTrainer(
    model=final_model,
    args=final_args,
    train_dataset=train_dataset,
    eval_dataset=valid_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Final training
final_trainer.train()

# Evaluate final model
eval_results = final_trainer.evaluate()
print(f"Final evaluation: {eval_results}")

os.makedirs("./results", exist_ok=True)
with open(f'./results/fold_{fold}_eval_results.json', 'w') as eval_results_file:
    json.dump(eval_results, eval_results_file, indent=4)

validation_prediction = final_trainer.predict(valid_dataset)
results_tp_fp = {
    "Actual": validation_prediction.label_ids.tolist(),
    "Predicted": np.argmax(validation_prediction.predictions, axis=1).tolist(),
    "Id": valid_dataset_id,
    "Labels": valid_dataset_row_author
}
results_df = pd.DataFrame.from_dict(results_tp_fp)
results_df.to_csv(f"./results/fold_{fold}_results.csv", index=False)

# Save the final model
final_trainer.save_model(f'./models/{fold}')
print("Model and tokenizer saved successfully.")



