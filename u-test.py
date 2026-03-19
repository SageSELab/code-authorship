
import pandas as pd 
import json
import glob
from scipy.stats import mannwhitneyu
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": "serif", 
    "font.serif": ["Times New Roman", "Liberation Serif"],
    'font.size': 10,
    'axes.titlesize': 14, 
    'axes.labelsize': 8,   
    'xtick.labelsize': 10,  
    'ytick.labelsize': 10, 
    'legend.fontsize': 8,
})


x_labels = [
    r"$\mathit{PbNN}$", r"$\mathit{CodeBERT}$", r"$\mathit{ContraBERT\_C}$", 
    r"$\mathit{ContraBERT\_C}$", r"$\mathit{GraphCodeBERT}$", r"$\mathit{UniXcoder}$", 
    r"$\mathit{DeepSeek-Coder}$", r"$\mathit{Code Llama}$"
]


best_config_resutls = pd.read_csv("best_config_results.csv")


def get_best_config(model, dataset):
    best_config = best_config_resutls[
        (best_config_resutls["model"] == model) & (best_config_resutls["dataset"] == dataset)
    ]
    return best_config.iloc[0]["config"]


models = best_config_resutls["model"].unique()


datasets = best_config_resutls["dataset"].unique()


def getf1(result_files):
    f1_scores = []
    for result_file in result_files:
        with open(result_file, "r") as f:
            result = json.load(f)
        f1_scores.append(result["eval_f1"])
    return f1_scores


datasets_names = ["GCJ-CPP", "GCJ-Java", "GCJ-Python", "Github-C", "Github-Java", "LeetCode"]


fig, axes = plt.subplots(2, 3, figsize=(20, 16))
axes = axes.flatten()
for index, dataset in enumerate(datasets):
    no_of_folds = 8 if dataset == 'gcj-cpp' else 10
    test_heatmap = [[0 for _ in range(len(models))] for _ in range(len(models))]
    for model1 in models:
        model1_best_config = get_best_config(model1, dataset)
        model1_results_files = glob.glob(f"./{dataset}/{model1}/results/{model1_best_config}_fold_*_eval_results.json")
        model1_f1_scores = getf1(model1_results_files)
        for model2 in models:
            model2_best_config = get_best_config(model2, dataset)
            model2_results_files = glob.glob(f"./{dataset}/{model2}/results/{model2_best_config}_fold_*_eval_results.json")
            model2_f1_scores = getf1(model2_results_files)
            u_statistic, p_value = mannwhitneyu(model1_f1_scores, model2_f1_scores, alternative='two-sided')
            test_heatmap[models.tolist().index(model1)][models.tolist().index(model2)] = p_value
    
    sns.heatmap(test_heatmap, xticklabels=x_labels, yticklabels=x_labels, annot=True, cmap="gray_r", fmt=".2f", vmin=0, vmax=0.05, cbar=False, ax=axes[index], linewidths=0.9,linecolor="gray", square=True)
    axes[index].set_title(f"U-Test Results of Models in {datasets_names[index]}")
    axes[index].set_xticklabels(x_labels, rotation=45, ha="right")


plt.subplots_adjust(hspace=0.4, wspace=0.01) 

plt.gcf().set_size_inches(18, 10) 

plt.savefig("u_test_results.pdf", bbox_inches="tight", dpi=300)





