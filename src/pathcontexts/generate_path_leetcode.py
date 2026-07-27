"""
Backwards-compatible wrapper: LeetCode path-context generation.

LeetCode solutions span several languages, so each row carries its own
'language' column. That is exactly what --language=auto does in the unified
generator.

Note: the original version of this script mapped languages as 'c++' and 'c#',
but the LeetCode dataset's language column actually contains 'cpp' and
'csharp', so it raised KeyError on the majority of rows. The unified generator
accepts both spellings (see tree_sitter_grammars._ALIASES).

Equivalent to:
  python generate_path_contexts.py --language=auto ...
"""

from generate_path_contexts import main

if __name__ == "__main__":
    main(default_language="auto")
