"""PyMuPDF (fitz) import helper — known SWIG DeprecationWarning on Python 3.12+."""

from __future__ import annotations

import warnings
from typing import Any


def load_fitz() -> Any:
    """Return the fitz module; suppress upstream SWIG deprecation noise at import."""
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message=r"builtin type SwigPy\w+ has no __module__ attribute",
        )
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message=r"builtin type swigvarlink has no __module__ attribute",
        )
        import fitz

    return fitz
