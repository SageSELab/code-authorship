import transformers
import torch
from pathlib import Path
from transformers import (AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments)
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, top_k_accuracy_score
import json
import os
import torch
torch.cuda.empty_cache()
from transformers import Trainer
import math
import sys

class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        outputs = model(**inputs)
        logits = outputs.get("logits")
        labels = inputs.get("labels")
        max_indices = torch.argmax(labels, dim=1)
        loss = torch.nn.functional.multi_margin_loss(logits, max_indices, margin=1)
        return (loss, outputs) if return_outputs else loss

class CodeStylometryDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def accuracy_throesh(y_pred, y_true, thresh=0.5, sigmoid=True): 
    return accuracy_score(np.argmax(y_true, axis=1),np.argmax(y_pred, axis=1))

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    return {'accuracy_thresh': accuracy_throesh(predictions, labels)}

model_ckpt = sys.argv[1]
model_name = sys.argv[2]
tokenizer_ckpt = sys.argv[3]

if not os.path.exists("./models"):
    os.makedirs("./models")

if not os.path.exists("./pred"):
    os.makedirs("./pred")

if not os.path.exists("./results"):
    os.makedirs("./results")

if not os.path.exists("./data"):
    os.makedirs("./data")

tokenizer = AutoTokenizer.from_pretrained(tokenizer_ckpt, problem_type="multi_label_classification")
    
def split_data(fold, type):
    df =  pd.read_csv(f"../data/fold_{fold}_{type}.csv").dropna()
    all_rows = []
    
    for index, row in df.iterrows():
        
        tokens = tokenizer.encode(row['code'])
        if len(tokens) <= 512:
            all_rows.append({'id':index, 'code': row['code'], 'author': row['author'], 'problem_url': row['problem_url'], 'solution_url': row['solution_url']})
            continue
        
        chunks = np.array_split(tokens, math.ceil(len(tokens) / 512))
        
        for chunk in chunks:
            all_rows.append({'id':index, 'code': tokenizer.decode(chunk.tolist(), skip_special_tokens=True), 'author': row['author'], 'problem_url': row['problem_url'], 'solution_url': row['solution_url']})
    
    df_splitted = pd.DataFrame(all_rows, columns = ['id', 'code', 'author', 'problem_url', 'solution_url'])
    df_splitted.to_csv(f'./data/fold_{fold}_{type}.csv',index=False)
    
    return df_splitted

for f in range(0, 10):
    df_train = split_data(f, "train")
    df_test =  split_data(f, "test")
    
    test_ids = df_test['id'].values.tolist()
    
    test_labels_ = df_test['author'].values.tolist()
    
    #drop columns
    drop_cols = ['id', 'problem_url', 'solution_url']
    df_test.drop(columns = drop_cols, inplace=True)
    df_train.drop(columns = drop_cols, inplace=True)
    
    df_train.rename(columns = {'author':'Y', 'code':'X'}, inplace = True)

    df_test.rename(columns = {'author':'Y', 'code':'X'}, inplace = True)

    df_train = pd.get_dummies(df_train, columns=["Y"])
    df_test = pd.get_dummies(df_test, columns=["Y"])

    dev_cols = [c for c in df_train.columns if c not in ["X", "Y"]]
    df_train["labels"] = df_train[dev_cols].values.tolist()
    df_test["labels"] = df_test[dev_cols].values.tolist()

    train_encodings = tokenizer(df_train["X"].values.tolist(), truncation=True, max_length=512)
    test_encodings = tokenizer(df_test["X"].values.tolist(), truncation=True, max_length=512)

    train_labels = [torch.tensor([float(f) for f in x]) for x in df_train["labels"].values.tolist()]
    test_labels = [torch.tensor([float(f) for f in x]) for x in df_test["labels"].values.tolist()]

    train_dataset = CodeStylometryDataset(train_encodings, train_labels)
    test_dataset = CodeStylometryDataset(test_encodings, test_labels)

    num_labels=len(dev_cols)
    model = AutoModelForSequenceClassification.from_pretrained(model_ckpt, num_labels=num_labels, problem_type="multi_label_classification").to('cuda')
    #model.config.pad_token_id = model.config.eos_token_id

    batch_size = 16
    # configure logging so we see training loss
    logging_steps = len(train_dataset) // batch_size

    args = TrainingArguments(
        output_dir="logs",
        overwrite_output_dir = True,
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=10,
        weight_decay=0.01,
        logging_steps=logging_steps,
        save_total_limit=1
    )


    trainer = CustomTrainer(model=model, args=args, train_dataset=train_dataset, eval_dataset=test_dataset, tokenizer=tokenizer,compute_metrics=compute_metrics)
    
    trainer.train()

    trainer.save_model(f"./models/{model_name}_fold{f}")
    
    trainer.evaluate()
    
    predition = trainer.predict(test_dataset)
    
    np.save(f"./pred/{model_name}_fold{f}.npy", predition.predictions)
    np.save(f"./pred/{model_name}_fold{f}_label_ids.npy", predition.label_ids)


    scores = []
    for i in range(1,11):
        scores.append(top_k_accuracy_score(np.argmax(predition.label_ids, axis=1), predition.predictions, k=i))

    results_tp_fp = {"Actual": [i+1 for i in np.argmax(predition.label_ids, axis=1)], 
               "Predicted": [i+1 for i in np.argmax(predition.predictions, axis=1)],
               "Id": test_ids,
               "Labels": test_labels_}
    results_df = pd.DataFrame.from_dict(results_tp_fp)

    results_df.to_csv(f"./results/{model_name}_fold_{f}.csv", index=False)

    json_object = json.dumps(scores, indent=4)

    with open(f"./results/{model_name}_fold_{f}.json", "w") as score_f:
        score_f.write(json_object)
        
    duplicate_ids = results_df[results_df['Id'].duplicated()]
    results_duplicate = {i: {'true': 0, 'false': 0} for i in duplicate_ids['Id'].unique()}
    
    for id in duplicate_ids['Id'].unique():
        sub_df = results_df[results_df['Id'] == id]
        for index, row in sub_df.iterrows():
            if row['Actual'] == row['Predicted']:
                results_duplicate[id]['true'] += 1
            else:
                results_duplicate[id]['false'] += 1
    
    total_correct = 0
    
    for index, row in results_df.iterrows():
        if row['Id'] in results_duplicate:
            continue
                
        if row['Actual'] == row['Predicted']:
            total_correct += 1
    
    chunk_correct_gt = 0
    chunk_correct_gt_eq = 0
    
    for id in results_duplicate:
        if results_duplicate[id]['true'] > results_duplicate[id]['false']:
            chunk_correct_gt += 1
        if results_duplicate[id]['true'] >= results_duplicate[id]['false']:
            chunk_correct_gt_eq += 1
    
    result = {'chunk_correct_gt':(total_correct + chunk_correct_gt)/len(results_df['Id'].unique()),
                'chunk_correct_gt_eq':(total_correct + chunk_correct_gt_eq)/len(results_df['Id'].unique()),
                'total_correct':scores[0]}
    
    json_object = json.dumps(result, indent=4)

    with open(f"./results/result_fold_{f}.json", "w") as res_f:
        res_f.write(json_object)


