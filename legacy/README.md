# Legacy scripts

These scripts were part of earlier iterations of the study. They are kept for
provenance — nothing in the documented pipeline calls them, and neither is
required to reproduce any result in the paper. They are **not** covered by the
Docker smoke test.

## `model.py`

The original hyperparameter search for the encoder models, driven by Optuna and
positional `sys.argv` arguments.

Superseded by **`../llm-fine-tuning.py`**, which takes the same approach but
reads the search grid from `../hyperparameter_combinations.csv`, uses named
`--flags`, and adds early stopping. `llm-fine-tuning.py` is what the
`run-*-cv.sh` scripts invoke and what produced the results reported in the
paper.

## `all-model-corrects.py`

An early version of the per-model correct-attribution collector, covering six
models across three datasets.

Superseded by **`../all-models-corrects.py`** (note the plural), which
`rq1-results.sh` calls. Besides the wider model and dataset coverage, the newer
script globs results as `{config}_fold_*_results.csv`. The pattern in this
legacy script — `fold_*_results.csv` — never matched the files the trainers
actually write, so it silently produced an empty result set.
