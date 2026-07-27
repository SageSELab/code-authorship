"""
Backwards-compatible wrapper: Python path-context generation.

The extraction logic now lives in generate_path_contexts.py, which handles
every dataset language. This wrapper is kept so the commands published with the
paper continue to work unchanged.

Equivalent to:
  python generate_path_contexts.py --language=python ...
"""

from generate_path_contexts import main

if __name__ == "__main__":
    main(default_language="python")
