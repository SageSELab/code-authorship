import json
import glob
import pandas as pd

datasets = ["LeetCode"]
models = ["PbNN", "CodeBERT", "GraphCodeBERT", "ContraBERT_C", "ContraBERT_G", "UniXcoder", "DeepSeek", "CodeLlama"]

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
            
            all_corrects[model].extend([f"{fold_no}_{i}" for i in df["Id"].values.tolist()])

with open("leetcode-all-models-corrects.json", "w") as f:
    json.dump(all_corrects, f, indent=4)
    

intersections = set(all_corrects["Code2Vec"])

for model in models[1:]:
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
    df = pd.read_csv(f"./LeetCode/data/fold_{fold_no}_test.csv")
    
    df = df.iloc[ids]
    
    df['fold_no'] = fold_no
    
    fold_wise_corrects_dfs.append(df)

fold_wise_corrects_df = pd.concat(fold_wise_corrects_dfs)

fold_wise_corrects_df["Id"] = range(1, len(fold_wise_corrects_df)+1)

fold_wise_corrects_df.to_csv("leetcode-all-models-corrects-intersection.csv", index=False)
