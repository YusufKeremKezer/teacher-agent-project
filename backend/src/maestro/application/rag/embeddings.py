from typing import Any
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from ...config import settings


def get_embedding_model(model_id: str, device: str = "cpu", **kwargs: Any) -> HuggingFaceEmbeddings:
    """Return a *HuggingFaceEmbeddings* instance for *model_id*.

    Extra ``kwargs`` are forwarded to the underlying class – useful for
    """
    return HuggingFaceEmbeddings(model_name=model_id, model_kwargs={"device": device})

if __name__ == "__main__":
    print(get_embedding_model(settings.RAG_TEXT_EMBEDDING_MODEL_ID).embed_query("Hello, world!"))