#!/usr/bin/env bash
#
# RQ1 tables and figures: how accurately does each model attribute authorship?
#
# Prerequisite: fine-tuning/training has been run, so that every
# {dataset}/{model}/results/ directory contains the per-fold
# "{config}_fold_{n}_eval_results.json" and "{config}_fold_{n}_results.csv"
# files. Missing model directories are reported by the scripts rather than
# silently producing empty tables.
#
# Usage:
#   ./rq1-results.sh
#
# Outputs (repository root):
#   best_config_results.csv                   per (dataset, model) best config
#   all_configs_results.csv                   every config, for the appendix
#   all_models_all_corrects.json              LeetCode per-model correct samples
#   all_models_correct_samples.csv            the same, joined back to snippets
#   u_test_results.pdf                        Mann-Whitney U comparisons

set -euo pipefail

cd "$(dirname "$0")"

echo "=== Aggregating k-fold results ==="
python k-fold-result-summary.py

echo "=== Collecting per-model correct attributions (LeetCode) ==="
python all-models-corrects.py

echo "=== LeetCode dataset statistics ==="
python leetcode-results.py

echo "=== Mann-Whitney U tests ==="
python u-test.py

echo "Done."
