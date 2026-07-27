#!/usr/bin/env bash
#
# RQ2 figures: what features do the models actually rely on?
#
# Prerequisite: the per-model explanations must already exist. Generate them by
# running the appropriate explainer inside each model directory first:
#
#   cd data/LeetCode/CodeBERT  && python ../../../src/rq2_features/lm-explainer.py \
#       --tokenizer=microsoft/codebert-base --h_config_no=1
#   cd data/LeetCode/DeepSeek  && python ../../../src/rq2_features/deepseek-explainer.py --h_config_no=5
#   cd data/LeetCode/CodeLlama && python ../../../src/rq2_features/codellama-explainer.py --h_config_no=1
#
# Usage:
#   src/rq2_features/rq2-results.sh                    # gcj-cpp/DeepSeek
#   src/rq2_features/rq2-results.sh gcj-python UniXcoder

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/../.." && pwd)"
cd "${REPO_ROOT}"

# t-SNE and the author word cloud are per-(dataset, model) figures; the paper
# reports them for DeepSeek on gcj-cpp.
DATASET="${1:-gcj-cpp}"
MODEL="${2:-DeepSeek}"

MODEL_DIR="${REPO_ROOT}/data/${DATASET}/${MODEL}"
if [ ! -d "$MODEL_DIR" ]; then
    echo "No such model directory: ${MODEL_DIR}" >&2
    exit 1
fi

# --- Necessity / sufficiency curves (all models, LeetCode) -------------------
echo "=== Necessity & sufficiency (Necessity_Sufficiency.pdf) ==="
python "${HERE}/necessity_sufficiency.py"

# --- Model orthogonality Venn diagram ---------------------------------------
echo "=== Orthogonality Venn diagram (leetcode_dataset_orthogonality.pdf) ==="
Rscript "${HERE}/venn-diagram.r"

# --- Per-model figures ------------------------------------------------------
# Both scripts read ./data, ./results and ./explanations relative to the model
# directory, so they must run from inside it.
echo "=== t-SNE projection for ${DATASET}/${MODEL} ==="
(cd "$MODEL_DIR" && python "${HERE}/tsne_plot.py")

echo "=== Author word cloud for ${DATASET}/${MODEL} ==="
(cd "$MODEL_DIR" && python "${HERE}/author_word_cloud.py")

echo "Done."
