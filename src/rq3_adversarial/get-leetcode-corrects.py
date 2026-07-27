import json
import glob
import pandas as pd

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from common.paths import DATA_DIR


datasets = ["LeetCode"]

# Per-model best hyperparameter configuration on LeetCode, as selected by
# k-fold-result-summary.py (highest mean eval_f1 across folds). The results
# files are named "{config}_fold_{n}_results.csv", so the config number is
# required to glob them -- a bare "fold_*_results.csv" pattern matches nothing.
models = [
    {"name": "PbNN",          "best_config": 3},
    {"name": "CodeBERT",      "best_config": 1},
    {"name": "GraphCodeBERT", "best_config": 3},
    {"name": "ContraBERT_C",  "best_config": 2},
    {"name": "ContraBERT_G",  "best_config": 3},
    {"name": "UniXcoder",     "best_config": 3},
    {"name": "DeepSeek",      "best_config": 5},
    {"name": "CodeLlama",     "best_config": 1},
]
model_names = [m["name"] for m in models]

all_corrects = {}

for dataset in datasets:
    for model_spec in models:
        model = model_spec["name"]
        csv_files = glob.glob(
            f"{DATA_DIR}/{dataset}/{model}/results/{model_spec['best_config']}_fold_*_results.csv"
        )

        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            
            df = df[df["Actual"] == df["Predicted"]]
            
            fold_no = int(csv_file.split("_")[-2])
            
            if model not in all_corrects:
                all_corrects[model] = []
            
            all_corrects[model].extend([f"{fold_no}_{i}" for i in df["Id"].values.tolist()])

with open("leetcode-all-models-corrects.json", "w") as f:
    json.dump(all_corrects, f, indent=4)
    

intersections = set(all_corrects[model_names[0]])

for model in model_names[1:]:
    intersections = intersections.intersection(all_corrects[model])

with open("leetcode-all-models-corrects-intersection.json", "w") as f:
    json.dump(list(intersections), f, indent=4)

intersections = list(intersections)

fold_wise_corrects = {}

for item in intersections:
    fold_no, id = item.split("_")
    
    if fold_no not in fold_wise_corrects:
        fold_wise_corrects[fold_no] = []
        
    fold_wise_corrects[fold_no].append(int(id)-1)
    

fold_wise_corrects_dfs = []

for fold_no, ids in fold_wise_corrects.items():
    df = pd.read_csv(DATA_DIR / "LeetCode" / "data" / f"fold_{fold_no}_test.csv")
    
    df = df.iloc[ids]
    
    df['fold_no'] = fold_no
    
    fold_wise_corrects_dfs.append(df)

fold_wise_corrects_df = pd.concat(fold_wise_corrects_dfs)

fold_wise_corrects_df["Id"] = range(1, len(fold_wise_corrects_df)+1)

fold_wise_corrects_df.to_csv("leetcode-all-models-corrects-intersection.csv", index=False)
