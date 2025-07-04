from langchain_core.documents import Document
from typing import List, Set, Tuple


def deduplicate_documents(docs: List[Document]) -> List[Document]:
    """Remove duplicate Documents while preserving original order.

    A Document is considered duplicate if both its *page_content* and *metadata*
    match another Document in the list. Only the first occurrence is kept.

    Args:
        docs: A list of Document instances that may contain duplicates.

    Returns:
        A new list of Document instances with duplicates removed.
    """
    seen: Set[Tuple[str, frozenset]] = set()
    unique_docs: List[Document] = []

    for doc in docs:
        key = (doc.page_content, frozenset(doc.metadata.items()))
        if key in seen:
            continue
        seen.add(key)
        unique_docs.append(doc)

    return unique_docs
