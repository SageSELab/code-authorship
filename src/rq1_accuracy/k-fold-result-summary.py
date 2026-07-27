
import pandas as pd 
import json
import glob

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from common.paths import DATA_DIR



datasets = [
    {
        "name": "gcj-cpp",
        "no_of_folds": 8
    },
    {
        "name": "gcj-java",
        "no_of_folds": 10
    },
    {
        "name": "gcj-python",
        "no_of_folds": 10
    },
    {
        "name": "github-c",
        "no_of_folds": 10
    },
    {
        "name": "github-java",
        "no_of_folds": 10
    },
    {
        "name": "LeetCode",
        "no_of_folds": 10
    }
]


models = [
    {
        "name": "PbNN",
        "no_of_configs": 5
    },
    {
        "name": "CodeBERT",
        "no_of_configs": 6
    },
    {
        "name": "ContraBERT_C",
        "no_of_configs": 6
    },
    {
        "name": "ContraBERT_G",
        "no_of_configs": 6
    },
    {
        "name": "GraphCodeBERT",
        "no_of_configs": 6
    },
    {
        "name": "UniXcoder",
        "no_of_configs": 6
    },
    {
        "name": "DeepSeek",
        "no_of_configs": 6
    },
    {
        "name": "CodeLlama",
        "no_of_configs": 1
    }
]


best_model_results = []
all_configs_results = []


for dataset in datasets:
    for model in models:
        model_results = []
        for config in range(1, model["no_of_configs"]+1):
            results_files = glob.glob(f"{DATA_DIR}/{dataset['name']}/{model['name']}/results/{config}_fold_*_eval_results.json")
            results = []
            for file in results_files:
                with open(file, "r") as f:
                    data = json.load(f)
                    data.pop('eval_loss', None)
                    data.pop('eval_runtime', None)
                    data.pop('eval_samples_per_second', None)
                    data.pop('eval_steps_per_second', None)
                    data.pop('epoch', None)
                    results.append(data)
            config_result = pd.DataFrame(results).mean().to_dict()
            config_result["model"] = model["name"]
            config_result["config"] = config
            model_results.append(config_result)
        model_result_df = pd.DataFrame(model_results).sort_values(by="eval_f1", ascending=False)
        model_result_df["dataset"] = dataset["name"]
        best_model_result = model_result_df.iloc[0].to_dict()
        best_model_results.append(best_model_result)
        all_configs_results.append(model_result_df)
        #break
    #break
            
                


pd.DataFrame(best_model_results).to_csv("best_config_results.csv", index=False)


pd.concat(all_configs_results).to_csv("all_configs_results.csv", index=False)





