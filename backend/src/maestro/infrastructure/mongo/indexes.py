
from .client import MongoClientWrapper


class MongoIndex:
    def __init__(
        self,
        retriever,
        mongodb_client: MongoClientWrapper,
    ) -> None:
        self.retriever = retriever
        self.mongodb_client = mongodb_client

    def create(
        self,
        embedding_dim: int,
        is_hybrid: bool = False,
    ) -> None:
        vectorstore = self.retriever.vectorstore

        vectorstore.create_vector_search_index(
            dimensions=embedding_dim,
        )
