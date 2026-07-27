"""
Shared Tree-sitter grammar loading for this replication package.

Every script that parses source code (path-context generation for PbNN, and
adversarial-rule verification) previously hardcoded its own relative path to a
compiled grammar, and each used a slightly different spelling for the same
language ('cpp' vs 'c++', 'csharp' vs 'c#'). This module centralises both.

Grammars are compiled by ``scripts/build-tree-sitter.sh``. Their location is
taken from the ``TREE_SITTER_SO_DIR`` environment variable (set inside the
Docker images), falling back to ``./tree-sitter-so`` relative to the repository
root so a manual local build keeps working.

This module targets the tree-sitter 0.21.x API (``Language(path, name)`` plus
``Parser.set_language``); see the pin in requirements.txt.
"""

import os
import warnings
from functools import lru_cache
from pathlib import Path

from tree_sitter import Language, Parser

# tree-sitter 0.21 warns that Language(path, name) is deprecated in favour of
# the 0.22+ Language(ptr, name). Using the path form is deliberate here — see
# the pin in requirements.txt — so the warning is noise, not a signal.
warnings.filterwarnings(
    "ignore",
    message=r"Language\(path, name\) is deprecated",
    category=FutureWarning,
)

REPO_ROOT = Path(__file__).resolve().parent

# Canonical language name -> (shared-object basename, tree-sitter symbol name).
# The symbol name is what the grammar registers internally and does not always
# match the repository name (c-sharp -> c_sharp).
_GRAMMARS = {
    "c": ("tree-sitter-c.so", "c"),
    "cpp": ("tree-sitter-cpp.so", "cpp"),
    "java": ("tree-sitter-java.so", "java"),
    "python": ("tree-sitter-python.so", "python"),
    "javascript": ("tree-sitter-javascript.so", "javascript"),
    "csharp": ("tree-sitter-c-sharp.so", "c_sharp"),
    "ruby": ("tree-sitter-ruby.so", "ruby"),
}

# Spellings that appear in the datasets and in the original scripts.
_ALIASES = {
    "c++": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "c#": "csharp",
    "c-sharp": "csharp",
    "c_sharp": "csharp",
    "js": "javascript",
    "py": "python",
    "python3": "python",
}

SUPPORTED_LANGUAGES = sorted(_GRAMMARS)


def grammar_dir():
    """Directory holding the compiled ``.so`` grammars."""
    return Path(os.environ.get("TREE_SITTER_SO_DIR", REPO_ROOT / "tree-sitter-so"))


def normalize_language(language):
    """Map any spelling used in this repo or its datasets to a canonical name."""
    key = str(language).strip().lower()
    key = _ALIASES.get(key, key)
    if key not in _GRAMMARS:
        raise ValueError(
            f"Unsupported language {language!r}. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES)}"
        )
    return key


@lru_cache(maxsize=None)
def get_language(language):
    """Load (and cache) the compiled grammar for ``language``."""
    name = normalize_language(language)
    so_name, symbol = _GRAMMARS[name]
    so_path = grammar_dir() / so_name
    if not so_path.exists():
        raise FileNotFoundError(
            f"Tree-sitter grammar not found: {so_path}\n"
            f"Build it with: scripts/build-tree-sitter.sh\n"
            f"(or set TREE_SITTER_SO_DIR to a directory that already has it)"
        )
    return Language(str(so_path), symbol)


@lru_cache(maxsize=None)
def get_parser(language):
    """Return a ``Parser`` configured for ``language``. Cached per language."""
    parser = Parser()
    parser.set_language(get_language(language))
    return parser
