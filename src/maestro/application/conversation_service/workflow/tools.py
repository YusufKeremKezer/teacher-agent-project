from langchain_community.tools import BraveSearch
from ....config import settings
from langchain_core.tools import create_retriever_tool
from ....application.rag.retrievers import get_retriever
from langchain_core.tools import tool


@tool(description="Searches the web using Brave Search API")
def brave_search_tool(query: str) -> str:
    brave_search = BraveSearch.from_api_key(api_key=settings.BRAVE_SEARCH_API_KEY
    , search_kwargs={"count": 3})
    return brave_search.run(query)
    


retriever = get_retriever(
    embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
    k=settings.RAG_TOP_K,
    device=settings.RAG_DEVICE)

retriever_tool = create_retriever_tool(
    retriever,
    name="retriever_tool",
    description="Retrieve relevant information from the database",
)








    








