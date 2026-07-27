# Data licensing and provenance

The MIT license in [`LICENSE`](LICENSE) covers the **code** in this repository.
It does not cover the source code *samples* in the `*/data/` directories, which
were written by third parties and are redistributed here for research
reproducibility only.

## Datasets

| Directory | Source | Language | Notes |
|---|---|---|---|
| `gcj-cpp/data` | Google Code Jam | C++ | Contest submissions, collected via the public GCJ archive. |
| `gcj-java/data` | Google Code Jam | Java | Same. |
| `gcj-python/data` | Google Code Jam | Python | Same. |
| `github-c/data` | GitHub | C | Files from public repositories. |
| `github-java/data` | GitHub | Java | Files from public repositories. |
| `LeetCode/data` | LeetCode | mixed | Publicly posted solutions; each row records `problem_url` and `solution_url`. |

Each CSV carries a pseudonymous `author` label. The Google Code Jam and LeetCode
labels are the handles their authors chose to publish under; the GitHub labels
derive from public commit authorship.

## Terms

- **Google Code Jam** submissions were published by their authors through
  Google's contest archive. Copyright remains with the individual authors.
- **GitHub** files come from public repositories under a range of open-source
  licenses. Per-file license terms were not normalised during collection; the
  files are included here only as classification inputs, not as reusable
  software.
- **LeetCode** solutions were posted publicly by their authors. LeetCode's terms
  of service govern access to the platform itself; the snippets are reproduced
  here for research reproducibility.

If you are an author of any snippet in this dataset and would like it removed,
please open an issue on this repository.

## If you redistribute

Do not treat these datasets as a general-purpose corpus. They exist so the
results in the paper can be checked. Re-use in other work should go back to the
original sources and apply their terms directly.

## Model weights

No pre-trained or fine-tuned weights are distributed here. CodeBERT,
GraphCodeBERT, UniXcoder, DeepSeek-Coder and Code Llama are downloaded from the
Hugging Face Hub under their own licenses at run time — note in particular that
Code Llama is covered by Meta's **Llama 2 Community License**, not an OSI
license. ContraBERT_C and ContraBERT_G are distributed by their authors; see
[`ContraBERT.md`](ContraBERT.md).
