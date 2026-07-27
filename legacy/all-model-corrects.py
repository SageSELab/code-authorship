import json
import glob
import pandas as pd

datasets = ["gcj-cpp", "gcj-python", "LeetCode"]
models = ["Code2Vec", "CodeBERT", "GraphCodeBERT", "ContraBERT_C", "ContraBERT_G", "UniXcoder"]

all_corrects = {}

for dataset in datasets:
    for model in models:
        csv_files = glob.glob(f"./{dataset}/{model}/results/fold_*_results.csv")
        
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            
            df = df[df["Actual"] == df["Predicted"]]
            
            fold_no = int(csv_file.split("_")[-2])
            
            if model not in all_corrects:
                all_corrects[model] = []
            
            all_corrects[model].extend([f"{dataset}_{fold_no}_{i}" for i in df["Id"].values.tolist()])

with open("all-corrects.json", "w") as f:
    json.dump(all_corrects, f, indent=4)
