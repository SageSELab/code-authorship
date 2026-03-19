import json
import glob
import pandas as pd

dataset = "LeetCode"
models = [
    {
        "name": "PbNN",
        "best_config": 3
    },
    {
        "name": "CodeBERT",
        "best_config": 1
    },
    {
        "name": "ContraBERT_C",
        "best_config": 2
    },
    {
        "name": "ContraBERT_G",
        "best_config": 3
    },
    {
        "name": "GraphCodeBERT",
        "best_config": 3
    },
    {
        "name": "UniXcoder",
        "best_config": 3
    },
    {
        "name": "DeepSeek",
        "best_config": 5
    },
    {
        "name": "CodeLlama",
        "best_config": 1
    }
]

all_corrects = {}

for model in models:
    csv_files = glob.glob(f"./{dataset}/{model['name']}/results/{model['best_config']}_fold_*_results.csv")
    
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        
        df.drop_duplicates(subset="Id", inplace=True, keep="first")
        
        df = df[df["Actual"] == df["Predicted"]]
        
        fold_no = int(csv_file.split("_")[-2])
        
        if model['name'] not in all_corrects:
            all_corrects[model['name']] = []
        
        all_corrects[model['name']].extend([f"{dataset}_{fold_no}_{i}" for i in df["Id"].values.tolist()])

with open(f"all_models_all_corrects.json", "w") as f:
    json.dump(all_corrects, f, indent=4)


with open("all_models_all_corrects.json") as f:
    data = json.load(f)


all_models_corrects = set(data['Code2Vec'])


for key in data:
    all_models_corrects = all_models_corrects.union(set(data[key]))


len(all_models_corrects)


all_models_corrects_sample = []


for sample in all_models_corrects:
    dataset, fold, sample_id = sample.split("_")
    df = pd.read_csv(f"./{dataset}/data/fold_{fold}_test.csv")
    
    sample_df = df[df['sample_id'] == int(sample_id)]
    sample_record = sample_df.to_dict(orient='records')[0]
    sample_record['location'] = sample
    sample_record['Code2Vec'] = True if sample in data['Code2Vec'] else False
    sample_record['CodeBERT'] = True if sample in data['CodeBERT'] else False
    sample_record['GraphCodeBERT'] = True if sample in data['GraphCodeBERT'] else False
    sample_record['ContraBERT_C'] = True if sample in data['ContraBERT_C'] else False
    sample_record['ContraBERT_G'] = True if sample in data['ContraBERT_G'] else False
    sample_record['UniXcoder'] = True if sample in data['UniXcoder'] else False
    sample_record['DeepSeek'] = True if sample in data['DeepSeek'] else False
    sample_record['CodeLlamaLoRA'] = True if sample in data['CodeLlamaLoRA'] else False
    all_models_corrects_sample.append(sample_record)


df = pd.DataFrame(all_models_corrects_sample)

df.to_csv("all_models_correct_samples.csv", index=False)