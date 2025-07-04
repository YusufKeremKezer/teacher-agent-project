from langchain_core.documents import Document
from loguru import logger

from maestro.application.data import deduplicate_documents, get_extraction_generator
from maestro.application.rag.retrievers import Retriever, get_retriever
from maestro.application.rag.splitters import Splitter, get_splitter
from maestro.config import settings
from ..domain.teachers import TeacherExtract
from ..infrastructure.mongo.client import MongoClientWrapper
from ..infrastructure.mongo.indexes import  MongoIndex


class LongTermMemoryCreator:
    def __init__(self, retriever: Retriever, splitter: Splitter) -> None:
        self.retriever = retriever
        self.splitter = splitter

    @classmethod
    def build_from_settings(cls) -> "LongTermMemoryCreator":
        retriever = get_retriever(
            embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            k=settings.RAG_TOP_K,
            device=settings.RAG_DEVICE,
        )
        splitter = get_splitter(chunk_size=settings.RAG_CHUNK_SIZE)

        return cls(retriever, splitter)

    def __call__(self, teachers: list[TeacherExtract]) -> None:
        if len(teachers) == 0:
            logger.warning("No teachers to extract. Exiting.")

            return

        # First clear the long term memory collection to avoid duplicates.
        with MongoClientWrapper(
            model=Document, collection_name=settings.MONGO_LONG_TERM_MEMORY_COLLECTION
        ) as client:
            client.clear_collection()

        extraction_generator = get_extraction_generator(teachers)
        for _, docs in extraction_generator:
            chunked_docs = self.splitter.split_documents(docs)


            self.retriever.vectorstore.add_documents(chunked_docs)

        self.__create_index()

    def __create_index(self) -> None:
        with MongoClientWrapper(
            model=Document, collection_name=settings.MONGO_LONG_TERM_MEMORY_COLLECTION
        ) as client:
            self.index = MongoIndex(
                retriever=self.retriever,
                mongodb_client=client,
            )
            self.index.create(
                is_hybrid=True, embedding_dim=settings.RAG_TEXT_EMBEDDING_MODEL_DIM
            )


class LongTermMemoryRetriever:
    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    @classmethod
    def build_from_settings(cls) -> "LongTermMemoryRetriever":
        retriever = get_retriever(
            embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            k=settings.RAG_TOP_K,
            device=settings.RAG_DEVICE,
        )

        return cls(retriever)

    def __call__(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)
