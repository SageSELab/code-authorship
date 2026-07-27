"""
Canonical locations inside this repository.

The pipeline scripts are run from several different working directories — the
repository root for the analysis steps, and `data/{dataset}/{model}/` for
training, explanation and attack steps. Resolving everything from ``__file__``
instead of the current directory means a script behaves the same wherever it is
invoked from.
"""

from pathlib import Path

# src/common/paths.py -> src/common -> src -> <repo root>
REPO_ROOT = Path(__file__).resolve().parents[2]

SRC_DIR = REPO_ROOT / "src"

#: The six datasets, each holding data/ plus one directory per model.
DATA_DIR = REPO_ROOT / "data"

#: Hand-curated experiment inputs: hyperparameter grids, rule categories.
CONFIG_DIR = REPO_ROOT / "config"

#: Compiled Tree-sitter grammars, when not overridden by TREE_SITTER_SO_DIR.
DEFAULT_TREE_SITTER_SO_DIR = REPO_ROOT / "tree-sitter-so"


def dataset_dir(name):
    """Path to a dataset directory, e.g. dataset_dir('LeetCode')."""
    return DATA_DIR / name


def fold_csv(dataset, fold, split):
    """Path to a dataset fold, e.g. fold_csv('LeetCode', 0, 'test')."""
    return DATA_DIR / dataset / "data" / f"fold_{fold}_{split}.csv"
