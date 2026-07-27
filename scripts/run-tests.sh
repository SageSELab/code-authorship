#!/usr/bin/env bash
#
# Run the adversarial-rule unit tests.
#
# These exercise the check_rule_* functions in adversarial_sample_verification.py
# against hand-written positive and negative examples in C++, Python and Java —
# the checks that decide whether a GPT-4-produced adversarial sample really
# applied the transformation it was asked to apply (RQ3).
#
# Usage:
#   scripts/run-tests.sh                          # all rules
#   scripts/run-tests.sh test_rule_13.py          # one rule
#
# Requires the Tree-sitter grammars; inside the Docker images they are already
# built and TREE_SITTER_SO_DIR is set. Outside, run scripts/build-tree-sitter.sh
# first.

set -euo pipefail

cd "$(dirname "$0")/.."

if [ "$#" -gt 0 ]; then
    exec python -m pytest "adversarial-rule-unit-tests/$1" -v
fi

exec python -m pytest adversarial-rule-unit-tests/ -v
