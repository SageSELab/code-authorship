#!/usr/bin/env bash
#
# Verify that this replication package's environment is complete and working.
#
# Runs on CPU in a few minutes and touches every class of dependency the study
# needs: Python packages, Tree-sitter grammars, R packages, the rule-checking
# unit tests, path-context generation, and one real (tiny) fine-tuning run.
#
# Usage:
#   docker compose run --rm caa-cpu scripts/smoke-test.sh
#   scripts/smoke-test.sh                       # on a host with deps installed
#
# Exits non-zero on the first failure and prints what to do about it.

set -uo pipefail

cd "$(dirname "$0")/.."
REPO_ROOT="$(pwd)"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

PASS=0
FAIL=0

pass() { printf '  \033[32mPASS\033[0m  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAIL=$((FAIL + 1)); }
step() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# ---------------------------------------------------------------------------
step "1/6  Python dependencies"
# ---------------------------------------------------------------------------
if python - <<'PY'
import importlib
import sys

# Every third-party module imported anywhere in the pipeline.
modules = [
    "captum", "datasets", "matplotlib", "numpy", "openai", "optuna", "pandas",
    "peft", "pytest", "requests", "scipy", "seaborn", "sklearn", "torch",
    "tqdm", "transformers", "tree_sitter", "wordcloud",
]
missing = [m for m in modules if not importlib.util.find_spec(m)]
if missing:
    print("missing: " + ", ".join(missing), file=sys.stderr)
    sys.exit(1)

import torch
import transformers
print(f"  torch {torch.__version__}, transformers {transformers.__version__}, "
      f"cuda={'yes' if torch.cuda.is_available() else 'no'}")
PY
then
    pass "all third-party imports resolve"
else
    fail "some packages are missing — pip install -r requirements.txt (or requirements-cpu.txt)"
fi

# ---------------------------------------------------------------------------
step "2/6  Tree-sitter grammars"
# ---------------------------------------------------------------------------
if python - <<'PY'
import sys

from tree_sitter_grammars import SUPPORTED_LANGUAGES, get_parser, grammar_dir

snippets = {
    "c":          "int main(void) { return 0; }",
    "cpp":        "int main() { int x = 1; return x; }",
    "java":       "class A { public static void main(String[] a) {} }",
    "python":     "def f(x):\n    return x + 1\n",
    "javascript": "function f(x) { return x + 1; }",
    "csharp":     "class A { static void Main() {} }",
    "ruby":       "def f(x)\n  x + 1\nend\n",
}

print(f"  grammar dir: {grammar_dir()}")
broken = []
for language in SUPPORTED_LANGUAGES:
    try:
        tree = get_parser(language).parse(snippets[language].encode())
        if tree.root_node.has_error or tree.root_node.child_count == 0:
            broken.append(f"{language} (parse error)")
    except Exception as exc:
        broken.append(f"{language} ({exc.__class__.__name__})")

if broken:
    print("  broken: " + ", ".join(broken), file=sys.stderr)
    sys.exit(1)
print(f"  {len(SUPPORTED_LANGUAGES)} grammars load and parse")
PY
then
    pass "all 7 grammars compile-load and parse"
else
    fail "grammars missing or ABI-mismatched — run scripts/build-tree-sitter.sh"
fi

# ---------------------------------------------------------------------------
step "3/6  R packages"
# ---------------------------------------------------------------------------
if Rscript -e 'library(venn); library(sets); library(jsonlite); cat("  venn, sets, jsonlite OK\n")' 2>/dev/null; then
    pass "R and the Venn-diagram packages are available"
else
    fail "R packages missing — needed by venn-diagram.r and orthogonality.r"
fi

# ---------------------------------------------------------------------------
step "4/6  Adversarial-rule unit tests"
# ---------------------------------------------------------------------------
TEST_LOG="$WORK_DIR/pytest.log"
if python -m pytest adversarial-rule-unit-tests/ -q >"$TEST_LOG" 2>&1; then
    pass "$(grep -oE '[0-9]+ passed[^=]*' "$TEST_LOG" | tail -n 1 | xargs)"
else
    fail "unit tests failed — see below"
    tail -n 25 "$TEST_LOG" | sed 's/^/       /'
fi

# ---------------------------------------------------------------------------
step "5/6  Path-context generation (PbNN input)"
# ---------------------------------------------------------------------------
if python generate_path_contexts.py \
        --language=cpp \
        --input_csv=./gcj-cpp/data/fold_0_test.csv \
        --output_json="$WORK_DIR/paths.json" \
        --limit=20 >/dev/null 2>&1 \
   && python - "$WORK_DIR/paths.json" <<'PY'
import json
import sys

records = json.load(open(sys.argv[1]))
assert len(records) == 20, f"expected 20 records, got {len(records)}"
assert all({"id", "path_contexts", "author"} <= set(r) for r in records), "bad schema"
assert any(r["path_contexts"] for r in records), "no path contexts extracted"
total = sum(len(r["path_contexts"]) for r in records)
print(f"  {len(records)} snippets -> {total} path contexts")
PY
then
    pass "path contexts extracted with the schema pbnn-training.py expects"
else
    fail "path-context generation failed"
fi

# ---------------------------------------------------------------------------
step "6/6  End-to-end fine-tuning (1 fold, 1 epoch, tiny subset)"
# ---------------------------------------------------------------------------
# Trains a real CodeBERT classifier on a 50-row slice of gcj-cpp. The point is
# not accuracy — it is that the trainer, tokenizer, metrics and result-writing
# path all work and produce the files the RQ1 scripts read.
TRAIN_DIR="$WORK_DIR/train/gcj-cpp/CodeBERT"
mkdir -p "$TRAIN_DIR" "$WORK_DIR/train/gcj-cpp/data"

python - "$REPO_ROOT" "$WORK_DIR/train/gcj-cpp/data" <<'PY'
import sys

import pandas as pd

repo, out = sys.argv[1], sys.argv[2]
for split in ("train", "test"):
    df = pd.read_csv(f"{repo}/gcj-cpp/data/fold_0_{split}.csv")
    # Keep 5 authors so the label space is small and every author appears in
    # both splits.
    authors = sorted(df["author"].unique())[:5]
    subset = df[df["author"].isin(authors)].groupby("author").head(10)
    subset.to_csv(f"{out}/fold_0_{split}.csv", index=False)
    print(f"  {split}: {len(subset)} rows, {subset['author'].nunique()} authors")
PY

cp "$REPO_ROOT/hyperparameter_combinations.csv" "$WORK_DIR/train/"
TRAIN_LOG="$WORK_DIR/train.log"

if (
    cd "$TRAIN_DIR" \
    && HF_HUB_OFFLINE=0 python "$REPO_ROOT/llm-fine-tuning.py" \
        --model_path=microsoft/codebert-base \
        --fold=0 \
        --max_context_length=128 \
        --h_config_no=1 \
        --num_train_epochs=1
) >"$TRAIN_LOG" 2>&1 \
   && [ -f "$TRAIN_DIR/results/1_fold_0_eval_results.json" ] \
   && [ -f "$TRAIN_DIR/results/1_fold_0_results.csv" ]; then
    pass "CodeBERT trained and wrote results/1_fold_0_{eval_results.json,results.csv}"
else
    fail "fine-tuning smoke run failed — see below"
    tail -n 25 "$TRAIN_LOG" | sed 's/^/       /'
fi

# ---------------------------------------------------------------------------
printf '\n\033[1m%s\033[0m\n' "Summary"
printf '  %d passed, %d failed\n\n' "$PASS" "$FAIL"

if [ "$FAIL" -gt 0 ]; then
    echo "Environment is NOT ready. See the failures above."
    exit 1
fi

echo "Environment is ready. Next: see the pipeline section of README.md."
