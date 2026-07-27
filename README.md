# Reassessing Code Authorship Attribution in the Era of Language Models

[![CI](https://github.com/SageSELab/code-authorship/actions/workflows/ci.yml/badge.svg)](https://github.com/SageSELab/code-authorship/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Data: see DATA-LICENSE](https://img.shields.io/badge/Data-see%20DATA--LICENSE-lightgrey.svg)](DATA-LICENSE.md)

Replication package for the TOSEM paper *"Reassessing Code Authorship
Attribution in the Era of Language Models."*

This artifact contains the six datasets (pre-split into folds), training and
evaluation scripts for all eight models, the explainability analysis, the
adversarial-attack pipeline, and a containerized environment so none of it
depends on the machine it was developed on.

> **New here?** Jump to [Quick start](#quick-start) — three commands get you a
> verified environment.

---

## Contents

- [What the study does](#what-the-study-does)
- [Quick start](#quick-start)
- [Requirements](#requirements)
- [Repository layout](#repository-layout)
- [Reproduction pipeline](#reproduction-pipeline)
- [Artifact provenance](#artifact-provenance)
- [External dependencies](#external-dependencies)
- [Transformation rules](#transformation-rules)
- [Known limitations](#known-limitations)
- [Figures](#figures)
- [Citation](#citation)

---

## What the study does

Code authorship attribution (CAA) asks: given a code snippet, who wrote it? The
paper evaluates how well modern pre-trained language models perform this task
compared to the prior path-based neural approach, what features they actually
key on, and how easily those decisions can be subverted by semantics-preserving
transformations.

**Models evaluated (8):**

| Model | Type | Checkpoint | Context | Configs |
|---|---|---|---|---|
| PbNN | Path-based neural network (baseline) | trained from scratch | — | 5 |
| CodeBERT | Encoder LM | `microsoft/codebert-base` | 512 | 6 |
| GraphCodeBERT | Encoder LM | `microsoft/graphcodebert-base` | 512 | 6 |
| ContraBERT_C | Encoder LM | Google Drive ([ContraBERT.md](ContraBERT.md)) | 512 | 6 |
| ContraBERT_G | Encoder LM | Google Drive ([ContraBERT.md](ContraBERT.md)) | 512 | 6 |
| UniXcoder | Encoder LM | `microsoft/unixcoder-base-nine` | 1024 | 6 |
| DeepSeek-Coder | Decoder LLM | `deepseek-ai/deepseek-coder-1.3b-instruct` | 2500 | 6 |
| Code Llama | Decoder LLM (LoRA) | `codellama/CodeLlama-7b-hf` | 2500 | 1 |

**Datasets (6):**

| Dataset | Language | Authors | Samples | Folds |
|---|---|---|---|---|
| `gcj-cpp` | C++ | 20 | 160 | 8 |
| `gcj-java` | Java | 74 | 2,202 | 10 |
| `gcj-python` | Python | 66 | 660 | 10 |
| `github-c` | C | 66 | 1,916 | 10 |
| `github-java` | Java | 39 | 2,667 | 10 |
| `LeetCode` | mixed | 198 | 4,753 | 10 |

**Research questions and the scripts that answer them:**

| RQ | Question | Entry point |
|---|---|---|
| RQ1 | How accurately do LMs attribute authorship, versus PbNN? | [`rq1-results.sh`](rq1-results.sh) |
| RQ2 | Which code features drive their predictions? | [`rq2-results.sh`](rq2-results.sh) |
| RQ3 | How robust are they to semantics-preserving transformations? | [`rq3-results.py`](rq3-results.py) |

---

## Quick start

```bash
git clone https://github.com/SageSELab/code-authorship.git
cd code-authorship

# Build the CPU image and verify the environment end to end.
docker compose build caa-cpu
docker compose run --rm caa-cpu scripts/smoke-test.sh
```

The smoke test checks six things and tells you exactly what is broken if any
fail:

1. every third-party Python package the pipeline imports resolves;
2. all seven Tree-sitter grammars compile-load and parse;
3. R and the Venn-diagram packages are available;
4. the adversarial-rule unit tests pass;
5. path-context extraction produces the schema PbNN expects;
6. a real (tiny) CodeBERT fine-tuning run completes and writes results.

For anything that needs a GPU — fine-tuning, the explainers, the attacks — build
the CUDA image instead:

```bash
docker compose build caa-gpu
docker compose run --rm caa-gpu bash
```

> **The GPU image requires an x86_64 host.** The pinned CUDA 12.1 wheels
> (`nvidia-*-cu12`) are published for x86_64 only, so `caa-gpu` cannot be built
> on Apple Silicon or other arm64 machines — the build stops early with a
> message saying so. `caa-cpu` builds and runs on both architectures.

Both images bind-mount the repository at `/workspace`, so every result, model
and figure lands in your checkout.

<details>
<summary>Running without Docker</summary>

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # or requirements-cpu.txt without a GPU
scripts/build-tree-sitter.sh           # compiles the Tree-sitter grammars
Rscript -e "install.packages(c('venn','sets','jsonlite'))"
scripts/smoke-test.sh
```

Python 3.10 is what the pins target. `scripts/build-tree-sitter.sh` needs `gcc`,
`g++` and `git`; the R scripts need a working `Rscript`.
</details>

---

## Requirements

**Software.** Docker (plus the NVIDIA Container Toolkit for the GPU image), or
Python 3.10 + R + a C/C++ compiler if you install natively.

**Hardware.**

| Task | Needs | Notes |
|---|---|---|
| Analysis, plotting, R figures, unit tests | CPU only | This is the `caa-cpu` image. |
| Path-context generation | CPU only | Single-threaded and slow — see below. |
| PbNN training | CPU works; GPU faster | Small model. |
| Encoder LMs (CodeBERT et al.) | ~8 GB VRAM | 125M parameters, batch size 16–32. |
| DeepSeek-Coder 1.3B | ~24 GB VRAM | 2,500-token context. |
| Code Llama 7B (LoRA) | ~40 GB VRAM | Batch size 2, 2,500-token context. |

**Disk.** ~1 GB for the repository, ~30 GB for the Hugging Face cache if you run
every model, and substantially more for checkpoints — each fine-tuning run saves
a model per fold per configuration.

**Time — read this before starting a full sweep.** The complete grid is 6
datasets × 8 models × up to 6 configurations × up to 10 folds: **thousands of
fine-tuning runs**, and weeks of single-GPU compute. It is not something to kick
off casually.

To spot-check a claim, reproduce one cell instead:

```bash
cd LeetCode/CodeBERT
../../run-codebert-cv.sh 10        # one model, one dataset, all configs and folds
```

Or narrow further, to a single fold and configuration:

```bash
cd LeetCode/CodeBERT
python ../../llm-fine-tuning.py --model_path=microsoft/codebert-base \
    --fold=0 --max_context_length=512 --h_config_no=1
```

---

## Repository layout

```
code-authorship/
├── docker/Dockerfile            # gpu and cpu build targets
├── docker-compose.yml           # caa-gpu / caa-cpu services
├── scripts/                     # environment setup and verification
│   ├── build-tree-sitter.sh     #   compile the 7 Tree-sitter grammars
│   ├── smoke-test.sh            #   verify the whole environment
│   ├── run-tests.sh             #   adversarial-rule unit tests
│   └── fetch-contrabert.sh      #   download the ContraBERT checkpoints
│
├── {dataset}/                   # gcj-cpp, gcj-java, gcj-python,
│   ├── data/                    #   github-c, github-java, LeetCode
│   │   ├── fold_N_train.csv     #   shipped: code, author, sample_id
│   │   ├── fold_N_test.csv
│   │   └── fold_N_*.json        #   generated: path contexts for PbNN
│   └── {model}/                 # PbNN, CodeBERT, ContraBERT_C, ContraBERT_G,
│       ├── data/                #   GraphCodeBERT, UniXcoder, DeepSeek, CodeLlama
│       ├── models/              # generated: fine-tuned checkpoints
│       ├── results/             # generated: per-fold metrics and predictions
│       └── explanations/        # generated: Captum attributions (RQ2)
│
├── llm-fine-tuning.py           # encoder LMs (CodeBERT, ContraBERT, ...)
├── deepseek-fine-tuning.py      # DeepSeek-Coder
├── codellama-fine-tuning.py     # Code Llama, LoRA
├── pbnn-training.py             # PbNN baseline
├── generate_path_contexts.py    # AST path contexts for PbNN (all languages)
├── run-*-cv.sh                  # per-model k-fold cross-validation drivers
│
├── rq1-results.sh               # RQ1 tables and figures
├── rq2-results.sh               # RQ2 figures
├── rq3-results.py               # RQ3 figures
│
├── *-explainer.py               # Captum attributions (RQ2)
├── adversarial-attack*.py       # RQ3 attacks
├── adversarial_sample_verification.py  # the 28 rule checkers
├── adversarial-rule-unit-tests/ # 25 test files covering those checkers
├── Prompts/{0..27}.txt          # the transformation prompts given to GPT-4o
│
├── attn_backend.py              # attention-backend selection helper
├── tree_sitter_grammars.py      # Tree-sitter grammar loading helper
└── legacy/                      # superseded scripts, kept for provenance
```

Each model directory ships only a `.gitkeep`; the `data/`, `models/`, `results/`
and `explanations/` subdirectories are created by the scripts on first run.

---

## Reproduction pipeline

### Step 1 — Data

Already done for you. Each `{dataset}/data/` directory ships the pre-split folds
as `fold_N_train.csv` / `fold_N_test.csv`, with columns `code`, `author` and
`sample_id` (LeetCode adds `language`, `problem_url`, `solution_url` and
`problem_id`).

Use these splits — re-splitting will produce different numbers than the paper.

### Step 2 — Path contexts (PbNN only)

The language models tokenize the CSVs directly. PbNN needs AST path contexts:

```bash
./generate_path_contexts.sh gcj-cpp        # one dataset
./generate_path_contexts.sh                # all six
```

Inside Docker the Tree-sitter grammars are already compiled. Natively, run
`scripts/build-tree-sitter.sh` first.

This is O(leaves²) per snippet and single-threaded — hours per dataset. Existing
`.json` outputs are skipped, so it is safe to interrupt and resume.

### Step 3 — Training and fine-tuning

Each model has a cross-validation driver, run from inside its dataset/model
directory. The argument is the number of folds (**8 for `gcj-cpp`, 10 for
everything else**).

```bash
cd LeetCode/CodeBERT
../../run-codebert-cv.sh 10
```

| Script | Model |
|---|---|
| `run-pbnn-cv.sh` | PbNN |
| `run-codebert-cv.sh` | CodeBERT |
| `run-graphcodebert-cv.sh` | GraphCodeBERT |
| `run-contrabert_c-cv.sh` | ContraBERT_C |
| `run-contrabert_g-cv.sh` | ContraBERT_G |
| `run-unixcoder-cv.sh` | UniXcoder |
| `run-deepseek-coder-cv.sh` | DeepSeek-Coder |
| `run-codellama-cv.sh` | Code Llama |

ContraBERT is not on the Hugging Face Hub — fetch it first with
`scripts/fetch-contrabert.sh`.

Each run writes into the model directory:

- `results/{config}_fold_{n}_eval_results.json` — accuracy, precision, recall, F1
- `results/{config}_fold_{n}_results.csv` — per-sample actual vs. predicted
- `models/{config}_{n}_model/` — the fine-tuned checkpoint

Hyperparameter grids: [`hyperparameter_combinations.csv`](hyperparameter_combinations.csv)
(learning rate × batch size, for the LMs) and
[`hyperparameter_combinations_pbnn.csv`](hyperparameter_combinations_pbnn.csv)
(hidden dimension, for PbNN).

### Step 4 — RQ1: attribution accuracy

```bash
./rq1-results.sh
```

Aggregates every `results/` directory into `best_config_results.csv` and
`all_configs_results.csv`, collects the per-model correct attributions, and runs
the Mann-Whitney U comparisons.

### Step 5 — RQ2: what the models rely on

First generate token attributions, from inside each model directory:

```bash
cd LeetCode/CodeBERT   && python ../../lm-explainer.py --tokenizer=microsoft/codebert-base --h_config_no=1
cd LeetCode/DeepSeek   && python ../../deepseek-explainer.py --h_config_no=5
cd LeetCode/CodeLlama  && python ../../codellama-explainer.py --h_config_no=1
```

`lm-explainer.py` covers all the encoder models; the two decoder models need
their own scripts because of how their embeddings and LoRA adapters load.

Then build the figures:

```bash
./rq2-results.sh                      # defaults to gcj-cpp/DeepSeek
./rq2-results.sh gcj-python UniXcoder # or any other (dataset, model)
```

Produces the necessity/sufficiency curves, the model-orthogonality Venn diagram,
the t-SNE projection, and the per-author word clouds.

### Step 6 — RQ3: adversarial robustness

Attacks are run on LeetCode only, because it is the one dataset where an
adversarial sample's functional equivalence can be *verified* — by submitting it
back to the judge.

**6a. Find the samples every model gets right.**

```bash
python get-leetcode-corrects.py
```

**6b. Generate adversarial variants with GPT-4o.**

```bash
export OPENAI_API_KEY=sk-...          # or put it in .env
python generate-adversarial-sample-gpt-4.py
```

Applies all 28 transformation prompts to each snippet. Resumable — already
generated files are skipped.

**6c. Verify the variants still work.**

```bash
export LEETCODE_CSRF_TOKEN=...        # from your browser cookies after logging in
export LEETCODE_SESSION=...
python submit2leetcode.py
python get-all-accepted-samples.py
python verify-adversarial-samples.py
```

`submit2leetcode.py` checks *functional* equivalence (does it still pass?).
`verify-adversarial-samples.py` checks *structural* correctness (did GPT-4o
actually apply the transformation it was asked to, and only that?), writing a
markdown report for every sample it rejects. Its rule checkers are covered by
`scripts/run-tests.sh`.

**6d. Attack the models.** Run from inside each model directory:

```bash
cd LeetCode/CodeBERT
python ../../adversarial-attack.py --tokenizer_path=microsoft/codebert-base \
    --max_context_length=512 --h_config=1 --model_name=CodeBERT
```

| Script | Applies to |
|---|---|
| `adversarial-attack.py` | all encoder LMs and DeepSeek-Coder |
| `adversarial-attack-codellama.py` | Code Llama (LoRA adapters) |
| `adversarial-attack-pbnn.py` | PbNN (path contexts rather than tokens) |

**6e. Build the figures.**

```bash
python rq3-results.py
```

---

## Artifact provenance

Where every non-obvious file comes from. **Shipped** means it is in this
repository; **generated** means a pipeline step produces it.

| File | Status | Produced by |
|---|---|---|
| `{dataset}/data/fold_*.csv` | shipped | — |
| `Prompts/{0..27}.txt` | shipped | — |
| `hyperparameter_combinations*.csv` | shipped | — |
| `{dataset}/data/fold_*.json` | generated | `generate_path_contexts.sh` (Step 2) |
| `{dataset}/{model}/results/*` | generated | `run-*-cv.sh` (Step 3) |
| `{dataset}/{model}/models/*` | generated | `run-*-cv.sh` (Step 3) |
| `{dataset}/{model}/explanations/*` | generated | `*-explainer.py` (Step 5) |
| `best_config_results.csv`, `all_configs_results.csv` | generated | `k-fold-result-summary.py` (Step 4) |
| `all_models_all_corrects.json`, `all_models_correct_samples.csv` | generated | `all-models-corrects.py` (Step 4) |
| `leetcode-all-models-corrects.json`, `…-intersection.json`, `…-intersection.csv` | generated | `get-leetcode-corrects.py` (Step 6a) |
| `Adversarial-Samples-GPT4/*.txt` | generated | `generate-adversarial-sample-gpt-4.py` (Step 6b) |
| `adversarial-samples-GPT4.csv`, `adversarial_samples_GPT4_accepted.csv` | generated | `get-all-accepted-samples.py` (Step 6c) |
| `adversarial_samples_GPT4_verified.csv` | generated | `verify-adversarial-samples.py` (Step 6c) |
| `positive_contributions.csv` | generated | `tsne_plot.py` (Step 5) |
| `adversarial_prompts_with_category.csv` | **required input, not yet in this repo** | hand-curated: maps each of the 28 rules to its category. Needed by `rq3-results.py`. |

### What is not in this repository

- **Trained checkpoints and per-fold results.** Hundreds of gigabytes.
  Regenerate with Step 3, or obtain them from the archive linked in the paper.
- **The adversarial samples used in the paper.** Steps 6b and 6c call
  non-deterministic third-party services, so regenerating them will not
  reproduce the exact set the paper reports on. To check the RQ3 numbers rather
  than the RQ3 method, use the shipped samples if you have them.
- **`adversarial_prompts_with_category.csv`.** `rq3-results.py` will fail
  without it. It is a small hand-curated mapping and matches the category table
  under [Transformation rules](#transformation-rules).

---

## External dependencies

| Dependency | Needed for | How it is supplied | If unavailable |
|---|---|---|---|
| Hugging Face Hub | CodeBERT, GraphCodeBERT, UniXcoder, DeepSeek-Coder, Code Llama | Downloaded on first use, cached in the `hf-cache` volume. `HF_TOKEN` only for rate limits. | Those models cannot be fine-tuned. |
| ContraBERT_C / ContraBERT_G | Two of the eight models | Google Drive; `scripts/fetch-contrabert.sh`, links in [ContraBERT.md](ContraBERT.md) | Skip those two models; the rest is unaffected. |
| OpenAI API | Generating adversarial samples (Step 6b) | `OPENAI_API_KEY` in `.env` | Use existing adversarial samples and skip to Step 6d. |
| LeetCode account | Functional verification (Step 6c) | `LEETCODE_CSRF_TOKEN` / `LEETCODE_SESSION` in `.env` | Use an existing accepted-samples CSV. |
| FlashAttention-2 | Speed for the two decoder models | Optional: `requirements-flash-attn.txt` | `attn_backend.py` falls back to PyTorch SDPA — same results, slower. |

Copy [`.env.example`](.env.example) to `.env` and fill in what you need. Docker
Compose loads it automatically; `.env` is gitignored.

---

## Transformation rules

The 28 semantics-preserving transformations used in RQ3. Each has a prompt given
to GPT-4o, a checker that validates the result, and unit tests.

| Category | Rules | Transformations | Checkers |
|---|---|---|---|
| Miscellaneous | 0–2 | remove comments; remove unused code; add logging statements | `check_rule_0` … `check_rule_2` |
| Statement | 3–5 | split declarations; merge declarations; reorder independent statements | `check_rule_3` … `check_rule_5` |
| Name | 6–7 | switch variable naming style; switch function naming style | `check_rule6_and_7` |
| Operator | 8–12 | swap relational operators; rewrite integer literals as expressions; change increment/decrement style | `check_rule_8` … `check_rule_12` |
| Data | 13–16 | integers to hex; chars to ASCII; strings to char arrays; booleans to integers | `check_rule_13` … `check_rule_16` |
| Loop | 17–18 | `for` ↔ `while` | `check_rule_17_and_18` |
| Control flow | 19–23 | `if-else` ↔ `switch`; `if-else` ↔ ternary; swap `if`/`else` bodies | `check_rule_19_and_20`, `check_rule_21` … `check_rule_23` |
| Function | 24–27 | swap parameter order; add a defaulted parameter; extract a function; reorder declarations | `check_rule_24` … `check_rule_27` |

Full prompt text is in [`Prompts/`](Prompts/) — `Prompts/N.txt` is rule `N`.
Checkers live in [`adversarial_sample_verification.py`](adversarial_sample_verification.py),
tests in [`adversarial-rule-unit-tests/`](adversarial-rule-unit-tests/):

```bash
scripts/run-tests.sh                  # all rules
scripts/run-tests.sh test_rule_13.py  # one rule
```

These run in CI on every commit, inside the same CPU image described above —
see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

[`Element-List.md`](Element-List.md) catalogues the code elements these
transformations operate on.

---

## Known limitations

- **The full sweep is impractical to re-run.** See the time estimates under
  [Requirements](#requirements). Reproduce individual cells instead.
- **Path-context generation is slow.** Single-threaded and quadratic in AST
  leaves. Budget hours per dataset.
- **RQ3 covers LeetCode only.** It is the one dataset where an adversarial
  sample's functional equivalence can be verified by an external judge. Whether
  the robustness findings generalise to the other five datasets is not
  established here.
- **Steps 6b and 6c depend on third-party services.** GPT-4o is not
  deterministic even at `temperature=0.1`, and the model behind that name
  changes over time, so regenerating adversarial samples will not reproduce the
  exact set used in the paper. LeetCode's submission API is unofficial and its
  cookie auth breaks periodically.
- **`rq3-results.py` needs `adversarial_prompts_with_category.csv`**, which is
  not currently in the repository — see
  [Artifact provenance](#artifact-provenance).
- **`legacy/` is not maintained** and is excluded from the smoke test. See
  [`legacy/README.md`](legacy/README.md).

---

## Figures

Full-resolution versions of figures that were reduced for the paper.

**Figure 1 — Distribution of code sample size across datasets**

![Figure 1](figures/dataset-distribution.jpg)

**Figure 3 — Performance improvement of LMs over PbNN**

![Figure 3](figures/performance_improvement_of_llms.png)

**Figure 4 — Mann-Whitney U test results**

![Figure 4](figures/u_test_results.jpg)

**Successful attacks per transformation category (RQ3)**

![Successful attacks](figures/successful_attacks_per_category.jpg)

**Code changes per category per model (RQ3)**

![Code changes](figures/code_changes_per_category_per_model.jpg)

**Author word clouds (RQ2, DeepSeek-Coder)**

![Word cloud](figures/authors_word_cloud_deepseek.jpg)

---

## Citation

```bibtex
@article{dipongkor2026reassessing,
  title     = {Reassessing Code Authorship Attribution in the Era of Language Models},
  author    = {Dipongkor, A. K. and Yao, Z. and Moran, K.},
  journal   = {ACM Transactions on Software Engineering and Methodology (TOSEM)},
  year      = {2026},
  publisher = {Association for Computing Machinery},
  note      = {Accepted}
}
```

See [`CITATION.cff`](CITATION.cff) for machine-readable metadata.

## License

Code is MIT-licensed ([`LICENSE`](LICENSE)). The datasets under `*/data/` are
third-party source code redistributed for research reproducibility — read
[`DATA-LICENSE.md`](DATA-LICENSE.md) before reusing them.
