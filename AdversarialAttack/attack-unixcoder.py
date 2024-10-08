
import torch
from transformers import (AutoTokenizer, AutoModelForSequenceClassification)
import pandas as pd
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
import math


model_path = './unixcoder_fine_tuned'
df = pd.read_csv('./adversarial_samples_v2.csv')

tokenizer = AutoTokenizer.from_pretrained(model_path, problem_type="multi_label_classification")
encodings = tokenizer(df["adv_code"].values.tolist(), truncation=True, max_length=512)

df['author_predicted'] = 0

model = AutoModelForSequenceClassification.from_pretrained(model_path,problem_type="multi_label_classification")

for index, row in df.iterrows():
    tokens = tokenizer(row["adv_code"])['input_ids']
    if len(tokens) <= 512:
        output = model(torch.tensor([tokens]))
        logits = output.logits
        probabilities = F.softmax(logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=-1).squeeze().item()
        df.iat[index,8] = predicted_class
    else:
        chunks = np.array_split(tokens, math.ceil(len(tokens) / 512))
        predicted_classes = []
        for chunk in chunks:
            output = model(torch.tensor([chunk]))
            logits = output.logits
            probabilities = F.softmax(logits, dim=-1)
            predicted_class = torch.argmax(probabilities, dim=-1).squeeze().item()
            predicted_classes.append(predicted_class)
        
        df.iat[index,8] = max(set(predicted_classes), key = predicted_classes.count)
        print(predicted_classes)
        print(max(set(predicted_classes), key = predicted_classes.count))


attack_success_df = df[df['author_predicted'] != df['author']]

attack_success_df.to_csv('attack_success_df.csv', index=False)





