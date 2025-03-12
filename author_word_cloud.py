
import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast
import matplotlib.patches as patches

df = pd.read_csv("positive_contributions.csv")

df['positive_contributions'] = df['positive_contributions'].apply(ast.literal_eval)

def clean_contributions(contributions):
    contributions = [re.sub(r"[^\x00-\x7F]+", "", contribution) for contribution in contributions]
    return [c for c in contributions if c != '<beginofsentence>']

df['positive_contributions'] = df['positive_contributions'].apply(clean_contributions)

n_rows = 1
n_cols = 4

# Create a figure with subplots
fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 20))  # Adjust figure size as needed
axes = axes.flatten()  # Flatten to easily iterate

for idx, (group, data) in enumerate(df.groupby('Actual')):
    if idx >= n_rows * n_cols:  # Stop if exceeding subplot limit
        break

    all_contributions = []
    for contributions in data['positive_contributions']:
        all_contributions.extend(contributions)

    word_counts = Counter(all_contributions)
    wordcloud = WordCloud(width=400, height=300, background_color='white').generate_from_frequencies(word_counts)

    ax = axes[idx]
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f"Author {group}", fontsize=12)

    # Add black border using a rectangle patch
    rect = patches.Rectangle(
        (0, 0), 1, 1, transform=ax.transAxes, linewidth=2, edgecolor='black', facecolor='none'
    )
    ax.add_patch(rect)

# Hide unused subplots if there are fewer than 20 authors
for i in range(idx + 1, n_rows * n_cols):
    axes[i].axis('off')

# Adjust spacing to remove large gaps
plt.subplots_adjust(wspace=0.05, hspace=-.1)  # Adjust these values to minimize row gaps
plt.tight_layout()
plt.savefig("authors_word_cloud_deepseek.pdf", dpi=300, bbox_inches='tight')
plt.show()





