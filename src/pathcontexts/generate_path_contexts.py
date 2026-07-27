"""
generate_path_contexts.py

Extract AST path contexts from a dataset fold, for training the path-based
neural network (PbNN) baseline.

Usage:
  python generate_path_contexts.py --language=cpp \
      --input_csv=gcj-cpp/data/fold_0_train.csv \
      --output_json=gcj-cpp/data/fold_0_train.json

What it does:
  1) Reads a CSV containing 'code' and 'author' columns (and possibly 'id', if
     it already exists). If 'id' is missing, it is created by assigning each row
     a unique integer ID starting at 1.
  2) For each row, parses the code snippet with Tree-sitter and extracts path
     contexts using an LCA-based approach constrained by max_height/max_width.
  3) Saves the result to JSON, one record per row:
       { "id": <ID>, "path_contexts": [[src, path, tgt], ...], "author": ... }

Languages:
  Pass an explicit --language for single-language datasets (gcj-cpp, gcj-java,
  gcj-python, github-c, github-java). Pass --language=auto for datasets whose
  rows carry their own 'language' column (LeetCode).

This script supersedes the earlier per-language copies
(generate_path_contexts_cpp.py, generate_path_contexts_python.py,
generate_path_leetcode.py), which are now thin wrappers around it. The
extraction logic is unchanged; only grammar loading and argument handling were
factored out.
"""

import argparse
import json

import pandas as pd

import sys as _sys
from pathlib import Path as _Path

# Scripts here are executed directly (often from a data/{dataset}/{model}/
# directory), so put src/ on the path to reach the shared helpers.
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))

from common.tree_sitter_grammars import SUPPORTED_LANGUAGES, get_parser


# ----------------------------------------------------------------------------
# 1. HELPER FUNCTIONS
# ----------------------------------------------------------------------------
def find_leaf_nodes(node):
    """
    Return all leaf nodes (those without children).
    """
    leaves = []
    if len(node.children) == 0:
        leaves.append(node)
    else:
        for child in node.children:
            leaves.extend(find_leaf_nodes(child))
    return leaves


def get_ancestry(node, limit=50):
    """
    Return a list of ancestors for the given node (including itself),
    up to a certain limit to prevent infinite loops in edge cases.
    """
    ancestors = []
    current = node
    steps = 0
    while current is not None and steps < limit:
        ancestors.append(current)
        current = current.parent
        steps += 1
    return ancestors


def extract_path_lca(start_node, end_node, max_height=8, max_width=3):
    """
    Builds a path from `start_node` to `end_node` by:
      1. Finding their lowest common ancestor (LCA).
      2. Climbing up from `start_node` to the LCA.
      3. Climbing up from `end_node` to the LCA.
      4. Combining those to form a path string.

    We enforce:
      - max_height: total steps up from start + end <= max_height
      - max_width : difference in columns <= max_width

    Returns a string like "token↑->token↑->LCA->token↓->token↓" or None if
    constraints fail.
    """
    # Gather ancestors
    start_ancestors = get_ancestry(start_node)
    end_ancestors = get_ancestry(end_node)

    # Find the first common ancestor (the LCA)
    lca = None
    for s_ancestor in start_ancestors:
        if s_ancestor in end_ancestors:
            lca = s_ancestor
            break
    if lca is None:
        return None  # should be rare in a well-formed AST

    # Check total path height
    dist_up = start_ancestors.index(lca)
    dist_down = end_ancestors.index(lca)
    if dist_up + dist_down > max_height:
        return None

    # Check column difference (width constraint)
    start_col = start_node.start_point[1]
    end_col = end_node.start_point[1]
    if abs(start_col - end_col) > max_width:
        return None

    # Build the upward path from start_node -> ... -> LCA
    up_segments = []
    cur = start_node
    while cur != lca:
        up_segments.append(cur.type + "↑")
        cur = cur.parent

    # Build the downward path from LCA -> ... -> end_node
    down_segments = []
    cur = end_node
    while cur != lca:
        down_segments.append(cur.type + "↓")
        cur = cur.parent

    # Combine: up_segments -> LCA -> reversed(down_segments)
    path_str = "->".join(up_segments + [lca.type] + down_segments[::-1])
    return path_str


def generate_path_contexts(code, parser, max_height=8, max_width=3):
    """
    Parse 'code' with Tree-sitter, then generate path contexts
    (source_token, path_string, target_token) for all leaf pairs.
    """
    tree = parser.parse(code.encode('utf-8'))
    root = tree.root_node
    leaves = find_leaf_nodes(root)
    path_contexts = []

    for i in range(len(leaves)):
        for j in range(i + 1, len(leaves)):
            start_leaf = leaves[i]
            end_leaf = leaves[j]
            path_str = extract_path_lca(
                start_node=start_leaf,
                end_node=end_leaf,
                max_height=max_height,
                max_width=max_width
            )
            if path_str:
                src_token = start_leaf.text.decode('utf-8', errors='ignore')
                tgt_token = end_leaf.text.decode('utf-8', errors='ignore')
                path_contexts.append((src_token, path_str, tgt_token))
    return path_contexts


# ----------------------------------------------------------------------------
# 2. MAIN SCRIPT (CSV -> JSON)
# ----------------------------------------------------------------------------
def build_records(df, language, max_height=8, max_width=3):
    """Turn a dataset fold into the list of records written to JSON."""
    records = []
    for _, row in df.iterrows():
        sample_id = row['id']
        code_snippet = str(row['code'])  # ensure string
        author = row['author']

        # 'auto' reads the per-row language column (LeetCode is multi-language).
        row_language = row['language'] if language == 'auto' else language
        parser = get_parser(row_language)

        path_ctxs = generate_path_contexts(
            code_snippet,
            parser,
            max_height=max_height,
            max_width=max_width
        )

        records.append({
            "id": str(sample_id),
            "path_contexts": path_ctxs,  # list of (src, path, tgt)
            "author": author
        })
    return records


def main(argv=None, default_language=None):
    parser_ = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    parser_.add_argument("--input_csv", type=str, required=True,
                         help="Path to the CSV file with 'code' and 'author' columns (and optional 'id').")
    parser_.add_argument("--output_json", type=str, required=True,
                         help="Where to save the JSON output.")
    parser_.add_argument("--language", type=str, default=default_language,
                         required=default_language is None,
                         help="Source language of the dataset: "
                              + ", ".join(SUPPORTED_LANGUAGES)
                              + ", or 'auto' to read each row's 'language' column.")
    parser_.add_argument("--max_height", type=int, default=8,
                         help="Maximum path height (sum of up+down steps).")
    parser_.add_argument("--max_width", type=int, default=3,
                         help="Maximum allowed column difference between leaf nodes.")
    parser_.add_argument("--limit", type=int, default=None,
                         help="Only process the first N rows. Intended for smoke tests.")
    args = parser_.parse_args(argv)

    # 1) Load CSV via pandas
    df = pd.read_csv(args.input_csv, encoding="utf-8")

    # 2) If 'id' column doesn't exist, generate it automatically
    if 'id' not in df.columns:
        df.insert(0, 'id', range(1, len(df) + 1))  # IDs start at 1

    # 3) Ensure we have the columns the chosen mode needs
    if 'code' not in df.columns or 'author' not in df.columns:
        raise ValueError("CSV must have 'code' and 'author' columns.")
    if args.language == 'auto' and 'language' not in df.columns:
        raise ValueError(
            f"--language=auto needs a 'language' column, which {args.input_csv} "
            f"does not have. Pass an explicit language instead."
        )

    if args.limit is not None:
        df = df.head(args.limit)

    # 4) For each row, extract path contexts using LCA-based logic
    data_for_json = build_records(df, args.language, args.max_height, args.max_width)

    # 5) Write to JSON
    with open(args.output_json, "w", encoding="utf-8") as out_f:
        json.dump(data_for_json, out_f, indent=2)

    print(f"Generated {len(data_for_json)} path_context entries.")
    print(f"Saved JSON to: {args.output_json}")


if __name__ == "__main__":
    main()
