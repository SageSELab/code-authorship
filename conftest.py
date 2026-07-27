"""
pytest configuration for this replication package.

The rule tests in ``tests/`` import the checkers with
``from adversarial_sample_verification import *``. That module lives in
``src/rq3_adversarial/``, and ``src/`` itself has to be importable for its
``common`` package. Both go on ``sys.path`` here, so the tests run from
anywhere:

    scripts/run-tests.sh
    python -m pytest tests/
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

for entry in (REPO_ROOT / "src", REPO_ROOT / "src" / "rq3_adversarial"):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))
