#!/usr/bin/env bash
#
# RQ1 tables and figures: how accurately does each model attribute authorship?
#
# Prerequisite: training has been run, so that every
# data/{dataset}/{model}/results/ directory contains the per-fold
# "{config}_fold_{n}_eval_results.json" and "{config}_fold_{n}_results.csv"
# files.
#
# Usage:
#   src/rq1_accuracy/rq1-results.sh
#
# Outputs land in the repository root:
#   best_config_results.csv                   per (dataset, model) best config
#   all_configs_results.csv                   every config, for the appendix
#   all_models_all_corrects.json              LeetCode per-model correct samples
#   all_models_correct_samples.csv            the same, joined back to snippets
#   u_test_results.pdf                        Mann-Whitney U comparisons

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Outputs are written relative to the working directory, so anchor at the root.
cd "${HERE}/../.."

echo "=== Aggregating k-fold results ==="
python "${HERE}/k-fold-result-summary.py"

echo "=== Collecting per-model correct attributions (LeetCode) ==="
python "${HERE}/all-models-corrects.py"

echo "=== LeetCode dataset statistics ==="
python "${HERE}/leetcode-results.py"

echo "=== Mann-Whitney U tests ==="
python "${HERE}/u-test.py"

echo "Done."
