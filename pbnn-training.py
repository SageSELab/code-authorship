"""
"""

import json
import csv
import argparse
import torch
import random
import numpy as np
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import pandas as pd

from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import precision_score, recall_score, f1_score

os.makedirs("./models", exist_ok=True)
os.makedirs("./results", exist_ok=True)


# ----------------------------------------------------------------------------
# 1. Reproducibility
# ----------------------------------------------------------------------------
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    # You can optionally enforce full determinism (slows down training):
    # torch.use_deterministic_algorithms(True)


# ----------------------------------------------------------------------------
# 2. DATASET DEFINITION
# ----------------------------------------------------------------------------

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


# ----------------------------------------------------------------------------
# 4. EVALUATION & COLLATE
# ----------------------------------------------------------------------------

def evaluate(model, dataloader, criterion, idx_to_author=None, device='cpu'):
    """
    Evaluate the model on a given dataloader, using the specified device (CPU or GPU).
    Returns:
      avg_loss, accuracy, precision, recall, f1,
      plus IDs and (optionally) actual/pred author strings.
    """
    model.eval()
    total_loss = 0
    correct = 0
    total = 0

    all_preds = []
    all_labels = []
    all_ids = []

    # If you want to store actual/pred author names:
    all_authors_str = []
    all_pred_authors_str = []

    with torch.no_grad():
        for batch in dataloader:
            ids, path_context_batch, labels = batch

            # Move data to the chosen device
            path_context_batch = path_context_batch.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(path_context_batch)
            loss = criterion(outputs, labels)
            total_loss += loss.item()

            preds = torch.argmax(outputs, dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

            # Store predictions
            all_ids.extend(ids)
            all_preds.append(preds.cpu())
            all_labels.append(labels.cpu())

    all_preds = torch.cat(all_preds).numpy()
    all_labels = torch.cat(all_labels).numpy()

    accuracy = correct / total
    precision = precision_score(all_labels, all_preds, average='macro', zero_division=0)
    recall    = recall_score(all_labels, all_preds, average='macro', zero_division=0)
    f1        = f1_score(all_labels, all_preds, average='macro', zero_division=0)
    avg_loss  = total_loss / len(dataloader)

    # Convert numeric preds/labels to author strings if idx_to_author is provided
    if idx_to_author is not None:
        for true_label, pred_label in zip(all_labels, all_preds):
            all_authors_str.append(idx_to_author[true_label])
            all_pred_authors_str.append(idx_to_author[pred_label])

    return (
        avg_loss,
        accuracy,
        precision,
        recall,
        f1,
        all_ids,
        all_authors_str,
        all_pred_authors_str
    )


def collate_fn(batch, vectorizer, max_paths=200):
    """
    batch: list of (id, path_contexts, label_idx)
    """
    id_list = []
    path_context_batches = []
    labels_list = []

    for (sample_id, contexts, label_idx) in batch:
        vec_ctx = vectorizer.vectorize(contexts)
        # Truncate/pad
        if vec_ctx.size(0) > max_paths:
            vec_ctx = vec_ctx[:max_paths, :]
        else:
            padding_needed = max_paths - vec_ctx.size(0)
            pad = torch.zeros((padding_needed, 3), dtype=torch.long)
            vec_ctx = torch.cat([vec_ctx, pad], dim=0)

        path_context_batches.append(vec_ctx)
        labels_list.append(label_idx)
        id_list.append(sample_id)

    path_context_batches = torch.stack(path_context_batches)  # (B, M, 3)
    labels = torch.tensor(labels_list, dtype=torch.long)
    return (id_list, path_context_batches, labels)


# ----------------------------------------------------------------------------
# 6. HELPER FUNCTIONS TO SAVE/LOAD VOCABS
# ----------------------------------------------------------------------------
def save_vocab(vocab, filepath):
    """
    Save the vocab's idx_to_token as JSON.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(vocab.idx_to_token, f, ensure_ascii=False, indent=2)


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


# ----------------------------------------------------------------------------
# 7. MAIN: TRAIN USING BEST HPARAMS, SAVE MODEL & VOCAB
# ----------------------------------------------------------------------------
def main():
    parser_ = argparse.ArgumentParser()
    parser_.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser_.add_argument("--fold", type=int, required=True,
                         help="Fold used as test partition for this run.")
    parser_.add_argument("--h_config_no", type=int, required=True,
                         help="Number of data folds total (e.g., if 5, then folds 0..4).")
    args = parser_.parse_args()
    
    seed = args.seed
    fold = args.fold
    h_config_no = args.h_config_no

    # 1) Set seed
    set_seed(seed)

    # 2) Decide on device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")


    # Read the test fold
    TEST_JSON = f"../data/fold_{fold}_test.json"
    TRAIN_JSON = f"../data/fold_{fold}_train.json"
    with open(TEST_JSON, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    test_dataset = PathContextDataset(test_data)

    with open(TRAIN_JSON, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    train_dataset = PathContextDataset(train_data)

    # 5) Build vocab from training data
    token_vocab = Vocab(special_tokens=["<PAD>", "<UNK>"])
    path_vocab  = Vocab(special_tokens=["<PAD>", "<UNK>"])

    for idx in range(len(train_dataset)):
        _, path_contexts, _ = train_dataset[idx]
        for (src, path, tgt) in path_contexts:
            token_vocab.add_token(src)
            token_vocab.add_token(tgt)
            path_vocab.add_token(path)

    # Create vectorizer
    vectorizer = PathContextVectorizer(token_vocab, path_vocab)

    # 6) Create DataLoaders
    max_paths = 200  # fixed or use a hyperparam
    train_loader = DataLoader(
        train_dataset,
        batch_size=128,
        shuffle=True,
        collate_fn=lambda b: collate_fn(b, vectorizer, max_paths)
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=128,
        shuffle=False,
        collate_fn=lambda b: collate_fn(b, vectorizer, max_paths)
    )
    
    # --------------------
    # Load Hyperparameters
    # --------------------
    config_df = pd.read_csv(f'../../hyperparameter_combinations_code2vec.csv')
    config = config_df[config_df['Configuration'] == h_config_no]
    hidden_dim = int(config['Hidden_Dim'].values[0])

    # 7) Build/Train model
    model = ProjectClassifier(
        n_tokens=len(vectorizer.token_vocab),
        n_paths=len(vectorizer.path_vocab),
        dim=hidden_dim,
        n_classes=len(train_dataset.author_to_idx)
    ).to(device)

    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    num_epochs = 40
    for _ in range(num_epochs):
        model.train()
        for _, path_context_batch, labels in train_loader:
            path_context_batch = path_context_batch.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(path_context_batch)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # 8) Evaluate on the test set
    (
        test_loss,
        test_acc,
        test_prec,
        test_rec,
        test_f1,
        test_ids,
        test_authors_str,
        test_pred_authors_str
    ) = evaluate(model, test_loader, criterion, idx_to_author=test_dataset.idx_to_author, device=device)

    eval_results = {
        "eval_loss": test_loss,
        "eval_accuracy": test_acc,
        "eval_precision": test_prec,
        "eval_recall": test_rec,
        "eval_f1": test_f1
    }

    # Save the metrics as JSON
    with open(f'./results/{h_config_no}_fold_{fold}_eval_results.json', 'w', encoding='utf-8') as eval_results_file:
        json.dump(eval_results, eval_results_file, indent=4)

    # 9) Generate CSV of predictions
    with open(f"./results/{h_config_no}_fold_{fold}_results.csv", "w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(["Id", "Actual", "Predicted"])
        for sample_id, actual_author, pred_author in zip(test_ids, test_authors_str, test_pred_authors_str):
            writer.writerow([sample_id, actual_author, pred_author])

    # 10) Save final model
    MODEL_PATH = f'./models/{h_config_no}_{fold}_model.pt'
    torch.save(model.state_dict(), MODEL_PATH)
    

    # 11) Save the vocabularies (token and path)
    TOKEN_VOCAB_PATH = f"./models/{h_config_no}_{fold}_token_vocab.json"
    PATH_VOCAB_PATH  = f"./models/{h_config_no}_{fold}_path_vocab.json"
    save_vocab(token_vocab, TOKEN_VOCAB_PATH)
    save_vocab(path_vocab, PATH_VOCAB_PATH)
    print(f"Token vocab saved to {TOKEN_VOCAB_PATH}")
    print(f"Path vocab saved to {PATH_VOCAB_PATH}")


if __name__ == "__main__":
    main()


