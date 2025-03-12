import json
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

dfs = []
h_config = 1
for fold in range(0, 8):
    test_df = pd.read_csv(f'./data/fold_{fold}_test.csv')
    test_results = pd.read_csv(f'./results/{h_config}_fold_{fold}_results.csv')
    test_results_corrects = test_results[test_results['Actual'] == test_results['Predicted']]
    test_results_corrects['positive_contributions'] = None

    for index, row in test_results_corrects.iterrows():
        with open(f'./explanations/{fold}_{index}_{row["Actual"]}_{row["Row_Id"]}_important_tokens.json') as f:
            explanations = json.load(f)
        
        positive_contributions = [element for element, contribution in explanations if contribution > 0]
        test_results_corrects.at[index, 'positive_contributions'] = positive_contributions[:int(len(positive_contributions)*0.30)]  # Get top 10 positive contributions
    dfs.append(test_results_corrects)

pd.concat(dfs).to_csv('./positive_contributions.csv', index=False)



df = pd.read_csv('positive_contributions.csv')


df['positive_contributions'] = df['positive_contributions'].apply(ast.literal_eval)


df['positive_contributions'] = df['positive_contributions'].apply(lambda x: ' '.join(x))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['positive_contributions'])

colors = plt.cm.tab20(np.linspace(0, 1, len(df['Actual'].unique())))

tsne = TSNE(n_components=2, random_state=42, perplexity=10, n_iter=5000, init='random')
X_tsne = tsne.fit_transform(X.toarray())

df['TSNE1'] = X_tsne[:, 0]
df['TSNE2'] = X_tsne[:, 1]

plt.figure(figsize=(4, 4))
for actual_class in df['Actual'].unique():
    subset = df[df['Actual'] == actual_class]
    plt.scatter(subset['TSNE1'], subset['TSNE2'], label=f'Class {actual_class}', alpha=0.9, color=colors[int(actual_class)])

plt.xlabel('TSNE1')
plt.ylabel('TSNE2')
plt.grid(True)
plt.tight_layout()
plt.savefig('tsne_plot.pdf', dpi=300)





