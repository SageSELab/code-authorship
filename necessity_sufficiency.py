
import json
import glob
import numpy as np
import matplotlib.pyplot as plt

models = ["CodeBERT", "ContraBERT_C", "ContraBERT_G", "GraphCodeBERT", "UniXcoder", "DeepSeek", "CodeLlamaLoRA"]

x_labels = [
    r"$\mathit{CodeBERT}$", r"$\mathit{ContraBERT\_C}$", 
    r"$\mathit{ContraBERT\_C}$", r"$\mathit{GraphCodeBERT}$", r"$\mathit{UniXcoder}$", 
    r"$\mathit{DeepSeek-Coder}$", r"$\mathit{Code Llama}$"
]

PPLCR_all_models = {} 

PPLA_all_models = {}


for model in models:
    file_pattern = f"./LeetCode/{model}/explanations/*_*_*_*_metrics.json"
    files = glob.glob(file_pattern)   

    PPLCR = {
        "0.1": 0,
        "0.2": 0,
        "0.3": 0,
        "0.4": 0,
        "0.5": 0
    }

    PPLA = {
        "0.1": 0,
        "0.2": 0,
        "0.3": 0,
        "0.4": 0,
        "0.5": 0,
        "0.6": 0,
        "0.7": 0,
        "0.9": 0
    }

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
        for key in PPLCR:
            PPLCR[key] += data[key]["PPLCR"]
        for key in PPLA:
            PPLA[key] += data[key]["PPLA"]


    for key in PPLCR:
        PPLCR[key] /= len(files)
    for key in PPLA:
        PPLA[key] /= len(files)


    for key in PPLCR:
        PPLCR[key] = np.exp(PPLCR[key])


    for key in PPLA:
        PPLA[key] = np.exp(PPLA[key])
    
    PPLCR_all_models[model] = PPLCR
    PPLA_all_models[model] = PPLA
    
    print(f"Model: {model}")

fig, axs = plt.subplots(1, 2, figsize=(7, 4))

for model, PPLCR in PPLCR_all_models.items():
    axs[0].plot(list(PPLCR.keys()), list(PPLCR.values()), marker='o', label=x_labels[models.index(model)])

axs[0].set_xlabel('Necessity Ratio')
axs[0].set_ylabel('Necessity Value')
axs[0].legend()

for model, PPLA in PPLA_all_models.items():
    axs[1].plot(list(PPLA.keys()), list(PPLA.values()), marker='o', label=x_labels[models.index(model)])

axs[1].set_xlabel('Sufficiency Ratio')
axs[1].set_ylabel('Sufficiency Value')
axs[1].legend()
plt.tight_layout()

plt.savefig("Necessity_Sufficiency.pdf", bbox_inches='tight', dpi=300)





