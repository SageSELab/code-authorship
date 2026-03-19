import pandas as pd
import argparse
import torch
from tqdm import tqdm
import json
import json
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
from torch.utils.data import Dataset

parser = argparse.ArgumentParser(description="Adversarial Attack on CodeBERT")

parser.add_argument("--sample_path", type=str, default="/Users/atish/Documents/KD-Orthogonality/Spitting-CAA-Study/GridSearch/Results/code2vec_adversarial_sample.json", help="Path to the sample.")
parser.add_argument("--h_config", type=int, default=3, help="Path to the hyperparameter config file no.")

args = parser.parse_args()
sample_path = args.sample_path
h_config = args.h_config

results_cache = {}

def get_actual_class(fold_no, sample_no):
    key = (h_config, fold_no)
    if key not in results_cache:
        results_cache[key] = pd.read_csv(f"./results/{h_config}_fold_{fold_no}_results.csv")
    result_df = results_cache[key]
    result_df = result_df[result_df["Id"] == int(sample_no)]
    return result_df["Predicted"].values[0]


class PathContextDataset(Dataset):
    """
    Reads a JSON file of the form:
      [
        {
          "id": <string or int>,
          "path_contexts": [
            ["src_token", "AST_path", "tgt_token"],
            ...
          ],
          "author": "author_name"
        },
        ...
      ]
    """
    def __init__(self, data):
        # Store all fields
        self.ids = [item["id"] for item in data]
        self.path_contexts_list = [item["path_contexts"] for item in data]
        self.authors = [item["author"] for item in data]

        # Build a label mapping
        self.author_to_idx = {author: idx for idx, author in enumerate(sorted(set(self.authors)))}
        self.idx_to_author = {v: k for k, v in self.author_to_idx.items()}

    def __len__(self):
        return len(self.path_contexts_list)

    def __getitem__(self, idx):
        return (
            self.ids[idx],
            self.path_contexts_list[idx],
            self.author_to_idx[self.authors[idx]]
        )


class Vocab:
    """
    Simple vocabulary class that tracks token <-> index mappings.
    """
    def __init__(self, special_tokens=None):
        self.token_to_idx = {}
        self.idx_to_token = []
        if special_tokens:
            for token in special_tokens:
                self.add_token(token)

    def add_token(self, token):
        if token not in self.token_to_idx:
            self.idx_to_token.append(token)
            self.token_to_idx[token] = len(self.idx_to_token) - 1

    def token2idx(self, token):
        # Return <UNK> if token not in vocab
        return self.token_to_idx.get(token, self.token_to_idx["<UNK>"])

    def __len__(self):
        return len(self.idx_to_token)


class PathContextVectorizer:
    """
    Converts path contexts (lists of (src, path, tgt)) to tensor indices.
    """
    def __init__(self, token_vocab, path_vocab):
        self.token_vocab = token_vocab
        self.path_vocab = path_vocab

    def vectorize(self, path_contexts):
        """
        path_contexts: [(src, path, tgt), ...]
        Returns a tensor of shape (num_contexts, 3).
        """
        indices = []
        for src, path, tgt in path_contexts:
            src_idx  = self.token_vocab.token2idx(src)
            path_idx = self.path_vocab.token2idx(path)
            tgt_idx  = self.token_vocab.token2idx(tgt)
            indices.append([src_idx, path_idx, tgt_idx])
        if not indices:
            # No contexts => return a single row of zeros
            indices = [[0, 0, 0]]
        return torch.tensor(indices, dtype=torch.long)


# ----------------------------------------------------------------------------
# 3. MODEL DEFINITION
# ----------------------------------------------------------------------------

class CodeVectorizer(nn.Module):
    def __init__(self, n_tokens, n_paths, dim, dropout_rate=0.2):
        super(CodeVectorizer, self).__init__()
        self.tokens_embed = nn.Embedding(n_tokens, dim)
        self.paths_embed = nn.Embedding(n_paths, dim)
        self.dropout = nn.Dropout(p=dropout_rate)
        self.transform = nn.Sequential(
            nn.Linear(3 * dim, dim),
            nn.Tanh()
        )
        self.attention = nn.Linear(dim, 1)

    def forward(self, contexts):
        starts, paths, ends = contexts
        starts = self.tokens_embed(starts)
        paths = self.paths_embed(paths)
        ends = self.tokens_embed(ends)

        concatenated = torch.cat((starts, paths, ends), dim=2)
        concatenated = self.dropout(concatenated)
        transformed = self.transform(concatenated)
        attn = F.softmax(self.attention(transformed), dim=1)
        aggregated = torch.sum(transformed * attn, dim=1)
        return aggregated


class ProjectClassifier(nn.Module):
    def __init__(self, n_tokens, n_paths, dim, n_classes, dropout_rate=0.2):
        super(ProjectClassifier, self).__init__()
        self.vectorization = CodeVectorizer(n_tokens, n_paths, dim, dropout_rate)
        self.classifier = nn.Linear(dim, n_classes)

    def forward(self, path_contexts_batch):
        # path_contexts_batch: (B, M, 3)
        starts, paths, ends = path_contexts_batch.unbind(dim=2)
        aggregated_context = self.vectorization((starts, paths, ends))
        outputs = self.classifier(aggregated_context)
        return outputs

def load_vocab(filepath):
    """
    Load a vocab from a JSON file containing idx_to_token.
    Reconstruct token_to_idx on the fly.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        idx_to_token = json.load(f)
    vocab = Vocab(special_tokens=[])  # we re-initialize
    vocab.idx_to_token = idx_to_token
    vocab.token_to_idx = {token: idx for idx, token in enumerate(idx_to_token)}
    return vocab

with open(sample_path, "r") as f:
    samples = json.load(f)

df = pd.read_csv("../../adversarial_samples_GPT4_accepted.csv")
df = df[df[f"Code2Vec"] == True]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


for sample in zip(samples, df.iterrows()):
    sample, (index, row) = sample
    
    _, fold_no, sample_no = sample["id"].split("_")
    actual_class = get_actual_class(fold_no, sample_no)
    # 1) Load vocab
    TOKEN_VOCAB_PATH = f"./models/{h_config}_{fold_no}_token_vocab.json"
    PATH_VOCAB_PATH  = f"./models/{h_config}_{fold_no}_path_vocab.json"
    token_vocab = load_vocab(TOKEN_VOCAB_PATH)
    path_vocab  = load_vocab(PATH_VOCAB_PATH)
    vectorizer = PathContextVectorizer(token_vocab, path_vocab)

    # 2) Rebuild the same model
    model = ProjectClassifier(
        n_tokens=len(token_vocab),
        n_paths=len(path_vocab),
        dim=128,  # must match what was used before
        n_classes=198
    )
    
    MODEL_PATH = f'./models/{h_config}_{fold_no}_model.pt'
    
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    
    model.eval()

    # 3) Vectorize new data
    new_contexts = sample["path_contexts"]
    vec_ctx = vectorizer.vectorize(new_contexts)
    # Possibly pad/truncate to match your training max_paths
    vec_ctx = vec_ctx.unsqueeze(0)  # add a batch dim

    # 4) Forward pass
    logits = model(vec_ctx)
    predicted_class_idx = logits.argmax(dim=1).item()
    print("Predicted class index:", predicted_class_idx)
    print("Actual class index:", actual_class)
    
    # Store results
    df.loc[index, ["predicted_class"]] = [predicted_class_idx]
    actual_class = get_actual_class(fold_no, sample_no)
    df.loc[index, ["actual_class", "correct"]] = [actual_class, predicted_class_idx == actual_class]
    
    if predicted_class_idx == actual_class:
        print("Attack failed!")
    else:
        print("Attack succeeded!")
    
# Save results
df.to_csv(f"./results/adversarial_samples_GPT4_accepted_Code2Vec_predictions.csv", index=False)


