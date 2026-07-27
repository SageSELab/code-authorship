"""
pytest configuration for this replication package.

The adversarial-rule tests live in a hyphenated directory
(``adversarial-rule-unit-tests/``) that is not an importable package, and they
import the checkers with ``from adversarial_sample_verification import *``.
Putting the repository root on ``sys.path`` here lets them run from anywhere:

    scripts/run-tests.sh
    python -m pytest adversarial-rule-unit-tests/
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
