#!/usr/bin/env bash
#
# Generate AST path contexts for every dataset fold. These JSON files are the
# input to src/training/pbnn-training.py (the PbNN baseline); the language
# models train directly from the CSVs and do not need this step.
#
# Usage:
#   scripts/build-tree-sitter.sh                      # once, unless in Docker
#   src/pathcontexts/generate_path_contexts.sh        # all datasets
#   src/pathcontexts/generate_path_contexts.sh gcj-cpp
#
# Runtime warning: path-context extraction is O(leaves^2) per snippet. The full
# sweep over all six datasets takes many hours on one core. Prefer generating
# only the dataset you intend to train on.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${HERE}/../.." && pwd)"
cd "${REPO_ROOT}"

PYTHON="${PYTHON:-python}"

# dataset<TAB>language<TAB>number-of-folds
#
# gcj-cpp has 8 folds; every other dataset has 10. 'auto' means the generator
# reads each row's own 'language' column, which only LeetCode carries.
DATASETS=$(
    cat <<'EOF'
gcj-cpp	cpp	8
gcj-java	java	10
gcj-python	python	10
github-c	c	10
github-java	java	10
LeetCode	auto	10
EOF
)

if [ "$#" -gt 0 ]; then
    DATASETS=$(echo "$DATASETS" | grep -E "^$1	") || {
        echo "Unknown dataset: $1" >&2
        echo "Choose one of: gcj-cpp gcj-java gcj-python github-c github-java LeetCode" >&2
        exit 1
    }
fi

while IFS=$'\t' read -r dataset language folds; do
    [ -n "$dataset" ] || continue
    echo "=== ${dataset} (${language}, ${folds} folds) ==="

    for i in $(seq 0 $((folds - 1))); do
        for split in train test; do
            out="./data/${dataset}/data/fold_${i}_${split}.json"
            if [ -f "$out" ]; then
                echo "[skip] ${out}"
                continue
            fi
            echo "[gen]  ${out}"
            "$PYTHON" "${HERE}/generate_path_contexts.py" \
                --language="${language}" \
                --input_csv="./data/${dataset}/data/fold_${i}_${split}.csv" \
                --output_json="${out}"
        done
    done
done <<<"$DATASETS"

echo "Done."
