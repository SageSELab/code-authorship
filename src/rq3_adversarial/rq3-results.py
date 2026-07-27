
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import difflib

import sys as _sys
from pathlib import Path as _Path

_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
from common.paths import CONFIG_DIR, DATA_DIR



models = ["PbNN","CodeBERT", "ContraBERT_C", "ContraBERT_G", "GraphCodeBERT", "UniXcoder", "DeepSeek", "CodeLlama"]


def calculate_line_changes(original_code: str, adversarial_code: str):
    """
    Calculate the number of lines added, deleted, and modified between two code snippets.

    :param original_code: String containing the original code.
    :param adversarial_code: String containing the adversarial code.
    :return: A dictionary containing counts of added, deleted, modified lines and percentage change.
    """
    original_lines = original_code.strip().split("\n")
    adversarial_lines = adversarial_code.strip().split("\n")

    diff = list(difflib.ndiff(original_lines, adversarial_lines))

    added_lines = sum(1 for line in diff if line.startswith("+ ") and not line.startswith("++"))
    deleted_lines = sum(1 for line in diff if line.startswith("- ") and not line.startswith("--"))
    modified_lines = min(added_lines, deleted_lines)  # Modified lines are those that appear in both added & deleted

    # Calculate the total change count
    total_changes = added_lines + deleted_lines - modified_lines

    # Compute percentage change based on the original code size
    total_original_lines = len(original_lines)
    percentage_change = (total_changes / total_original_lines) if total_original_lines > 0 else 0

    return percentage_change


adversarial_prompts = pd.read_csv(CONFIG_DIR / "adversarial_prompts_with_category.csv")


plt.rcParams.update({
    "font.family": "serif",  # Use serif fonts like ACM
    "font.serif": ["Times New Roman", "Liberation Serif"],  # ACM-like font
    'font.size': 10,
    'axes.titlesize': 10,   # Title font size
    'axes.labelsize': 8,   # Axes labels font size
    'xtick.labelsize': 8,  # X-tick labels font size
    'ytick.labelsize': 8,  # Y-tick labels font size
    'legend.fontsize': 8,  # Legend font size
})


def find_category(rule):
    adversarial_prompts[adversarial_prompts["id"] == rule]
    return adversarial_prompts[adversarial_prompts["id"] == rule]["category"].values[0]


model_names = [
    r"$\mathit{PbNN}$", r"$\mathit{CodeBERT}$", r"$\mathit{ContraBERT\_C}$", 
    r"$\mathit{ContraBERT\_C}$", r"$\mathit{GraphCodeBERT}$", r"$\mathit{UniXcoder}$", 
    r"$\mathit{DeepSeek-Coder}$", r"$\mathit{Code Llama}$"
]


# Define a publication-quality color palette
color_palette = sns.color_palette("Set2", 8)  # Use "Set2" for distinct colors

# Create subplots: 2 rows, 4 columns
fig, axes = plt.subplots(2, 4, figsize=(7, 4), constrained_layout=True)

# Flatten axes for easy iteration
axes = axes.flatten()

for idx, model in enumerate(models):
    path = f"./LeetCode/{model}/results/verified_atacks.csv"
    df = pd.read_csv(path)
    df["category"] = df["rule"].apply(find_category)
    
    overall_success_rate = len(df[df['correct'] == False]) / len(df)

    # Count successful and total attacks per category
    successful_attacks = df[df['correct'] == False]['category'].value_counts().sort_index()
    total_attacks = df['category'].value_counts().sort_index()
    attack_ratios = (successful_attacks / total_attacks).fillna(0)  # Avoid division errors
    
    # Assign colors based on unique categories
    unique_categories = attack_ratios.index
    color_map = {category: color_palette[i % len(color_palette)] for i, category in enumerate(unique_categories)}

    # Plot on the corresponding subplot
    ax = axes[idx]
    attack_ratios.plot(kind="bar", ax=ax, color=[color_map[cat] for cat in unique_categories], edgecolor="black")
    
    ax.set_title(f"{model_names[idx]} ({overall_success_rate:.2%})", fontsize=8)
    ax.set_xlabel("")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    # ax.set_ylabel("Successful Attack Ratio")
    
    # Rotate x-axis labels for better readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

# Adjust layout and save the figure
#plt.suptitle("Successful Attack Ratios per Category Across Models", fontsize=16)
fig.text(0.5, 0.02, "Category", ha='center')  # Global x-label
fig.text(0.001, 0.5, "Attack Success Ratio", va='center', rotation='vertical')  # Global y-label
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("successful_attacks_per_category.pdf", dpi=300)
plt.show()


def find_code_snippet(location):
    _, fold, sample_id = location.split('_')
    sample_df = pd.read_csv(DATA_DIR / "LeetCode" / "data" / f"fold_{fold}_test.csv")
    sample_df = sample_df[sample_df['sample_id'] == int(sample_id)]
    return sample_df['code'].values[0]


df['original_code'] = df['location'].apply(find_code_snippet)


df['percentage_change'] = df.apply(lambda row: calculate_line_changes(row['original_code'], row['adversarial_code']), axis=1)


verified_samples_df = pd.read_csv("./adversarial_samples_GPT4_accepted_verified.csv")


verified_samples_df = verified_samples_df[verified_samples_df['valid_transformation']]


import os
for index, row in verified_samples_df.iterrows():
    original_code = find_code_snippet(row['location'])
    if os.path.exists(f"./VerifiedOriginalSamples/{row['location']}.txt"):
        continue
    with open(f"./VerifiedOriginalSamples/{row['location']}.txt", 'w') as f:
        f.write(original_code)


def find_original_code(location):
    with open(f"./VerifiedOriginalSamples/{location}.txt", 'r') as f:
        return f.read()


# Define a publication-quality color palette
color_palette = sns.color_palette("Set2", 8)  # Use "Set2" for distinct colors

# Create subplots: 2 rows, 4 columns
fig, axes = plt.subplots(2, 4, figsize=(7, 4), constrained_layout=True)

# Flatten axes for easy iteration
axes = axes.flatten()

for idx, model in enumerate(models):
    path = f"./LeetCode/{model}/results/verified_atacks.csv"
    df = pd.read_csv(path)
    df = df[df['correct'] == False]
    df["category"] = df["rule"].apply(find_category)
    df['original_code'] = df['location'].apply(find_original_code)
    df['percentage_change'] = df.apply(lambda row: calculate_line_changes(row['original_code'], row['adversarial_code']), axis=1)
    

    # Count successful and total attacks per category
    # successful_attacks = df[df['correct'] == False]['category'].value_counts().sort_index()
    # total_attacks = df['category'].value_counts().sort_index()
    
    attack_ratios = df[['category', 'percentage_change']].groupby('category').mean()['percentage_change'] # Avoid division errors
    
    # Assign colors based on unique categories
    unique_categories = attack_ratios.index
    color_map = {category: color_palette[i % len(color_palette)] for i, category in enumerate(unique_categories)}

    # Plot on the corresponding subplot
    ax = axes[idx]
    attack_ratios.plot(kind="bar", ax=ax, color=[color_map[cat] for cat in unique_categories], edgecolor="black")
    
    ax.set_title(f"{model_names[idx]}", fontsize=8)
    ax.set_xlabel("")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    
    # Rotate x-axis labels for better readability
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

# Adjust layout and save the figure
#plt.suptitle("Successful Attack Ratios per Category Across Models", fontsize=16)
fig.text(0.5, 0.01, "Category", ha='center')  # Global x-label
fig.text(0.0001, 0.5, "Amount of Change (%)", va='center', rotation='vertical')  # Global y-label
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("code_changes_per_category_per_model.pdf", dpi=300)
plt.show()


verified_samples_df['original_code'] = verified_samples_df['location'].apply(find_original_code)


verified_samples_df['category'] = verified_samples_df['rule'].apply(find_category)


verified_samples_df['percentage_change'] = verified_samples_df.apply(lambda row: calculate_line_changes(row['original_code'], row['adversarial_code']), axis=1)


attack_ratios = df[['category', 'percentage_change']].groupby('category').mean()['percentage_change']


plt.figure(figsize=(4, 3))
attack_ratios.plot(kind="bar", color=[color_map[cat] for cat in unique_categories], edgecolor="black")
plt.grid(axis='y', linestyle='--', alpha=0.6)

plt.xlabel("Category", fontsize=10)
plt.ylabel("Amount of Code Change (%)", fontsize=10)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("code_changes_per_category.pdf", dpi=300)
plt.show()





