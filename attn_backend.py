"""
Attention-backend selection for the decoder models (Code Llama, DeepSeek-Coder).

The fine-tuning, explanation and attack scripts for these two models were
written on a machine with FlashAttention-2 installed and passed
``attn_implementation="flash_attention_2"`` unconditionally. ``flash-attn`` is
a heavy, GPU-only, source-built package that is not installable from
requirements.txt (it needs torch present at build time and Ampere-or-newer
hardware), so on any other machine those calls fail outright with:

    ImportError: FlashAttention2 has been toggled on, but it cannot be used ...

This helper picks the fastest backend actually available, preserving the
original behaviour wherever FlashAttention-2 is installed:

    flash_attention_2  ->  sdpa  ->  eager

To reproduce the paper's exact configuration, install FlashAttention-2 into the
GPU image (see requirements-flash-attn.txt) and this returns
"flash_attention_2" as before. Numerical results are unaffected by the choice;
only speed and memory use change.
"""

import os
import warnings

_CACHED = None


def _flash_attention_available():
    try:
        import flash_attn  # noqa: F401
    except ImportError:
        return False

    try:
        import torch
    except ImportError:  # pragma: no cover - torch is a hard dependency
        return False

    # FlashAttention-2 requires an Ampere (SM 8.0) or newer GPU.
    if not torch.cuda.is_available():
        return False
    major, _ = torch.cuda.get_device_capability()
    return major >= 8


def _sdpa_available():
    try:
        import torch
        return hasattr(torch.nn.functional, "scaled_dot_product_attention")
    except ImportError:  # pragma: no cover
        return False


def attn_implementation():
    """
    Return the attention implementation to pass to ``from_pretrained``.

    Override with the ATTN_IMPLEMENTATION environment variable
    (e.g. ATTN_IMPLEMENTATION=eager) to force a specific backend.
    """
    global _CACHED

    override = os.environ.get("ATTN_IMPLEMENTATION")
    if override:
        return override

    if _CACHED is not None:
        return _CACHED

    if _flash_attention_available():
        _CACHED = "flash_attention_2"
    elif _sdpa_available():
        _CACHED = "sdpa"
        warnings.warn(
            "FlashAttention-2 is unavailable; falling back to PyTorch SDPA. "
            "This is slower and uses more memory than the paper's setup, but "
            "produces the same results. See requirements-flash-attn.txt.",
            RuntimeWarning,
        )
    else:
        _CACHED = "eager"
        warnings.warn(
            "Neither FlashAttention-2 nor SDPA is available; falling back to "
            "eager attention. Expect this to be substantially slower.",
            RuntimeWarning,
        )

    return _CACHED
