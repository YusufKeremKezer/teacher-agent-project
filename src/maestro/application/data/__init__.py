"""Data extraction utilities exposed at package level.

This subpackage provides helpers for extracting and post-processing documents
related to teachers. To make them easy to import, the most commonly used
functions are re-exported here::

    from maestro.application.data import deduplicate_documents, get_extraction_generator
"""

from .extract import get_extraction_generator  # noqa: F401
from .deduplicate_documents import deduplicate_documents  # noqa: F401

__all__: list[str] = [
    "deduplicate_documents",
    "get_extraction_generator",
] 