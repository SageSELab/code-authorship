#!/usr/bin/env bash
#
# RQ2 figures: what features do the models actually rely on?
#
# Prerequisite: the per-model explanations must already exist. Generate them by
# running the appropriate explainer inside each model directory first:
#
#   cd LeetCode/CodeBERT   && python ../../lm-explainer.py --tokenizer=microsoft/codebert-base --h_config_no=1
#   cd LeetCode/DeepSeek   && python ../../deepseek-explainer.py --h_config_no=5
#   cd LeetCode/CodeLlama  && python ../../codellama-explainer.py --h_config_no=1
#
# Usage:
#   ./rq2-results.sh                    # defaults to gcj-cpp/DeepSeek for the
#                                       # t-SNE and word-cloud figures
#   ./rq2-results.sh gcj-python UniXcoder

set -euo pipefail

cd "$(dirname "$0")"
REPO_ROOT="$(pwd)"

# t-SNE and the author word cloud are per-(dataset, model) figures; the paper
# reports them for DeepSeek on gcj-cpp.
DATASET="${1:-gcj-cpp}"
MODEL="${2:-DeepSeek}"

MODEL_DIR="${REPO_ROOT}/${DATASET}/${MODEL}"
if [ ! -d "$MODEL_DIR" ]; then
    echo "No such model directory: ${MODEL_DIR}" >&2
    exit 1
fi

# --- Necessity / sufficiency curves (all models, LeetCode) -------------------
echo "=== Necessity & sufficiency (Necessity_Sufficiency.pdf) ==="
python necessity_sufficiency.py

# --- Model orthogonality Venn diagram ---------------------------------------
echo "=== Orthogonality Venn diagram (leetcode_dataset_orthogonality.pdf) ==="
Rscript venn-diagram.r

# --- Per-model figures ------------------------------------------------------
# Both scripts read ./data, ./results and ./explanations relative to the model
# directory, so they must run from inside it.
echo "=== t-SNE projection for ${DATASET}/${MODEL} ==="
(cd "$MODEL_DIR" && python "${REPO_ROOT}/tsne_plot.py")

echo "=== Author word cloud for ${DATASET}/${MODEL} ==="
(cd "$MODEL_DIR" && python "${REPO_ROOT}/author_word_cloud.py")

echo "Done."
