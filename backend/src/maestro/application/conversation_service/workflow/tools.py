from langchain_community.tools import BraveSearch
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from ....config import settings
from langchain_core.tools import BaseTool
from typing import Optional
from langchain_core.callbacks.manager import CallbackManagerForToolRun
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


@tool(description="Search within a specific website using Brave")
def site_specific_search(query: str, site: str) -> str:
    """
    Searches within a specific website by adding 'site:' filter.
    
    Args:
        query: Search query
        site: Domain to restrict search to (e.g., 'blog.samaltman.com')
    """
    full_query = f"{query} site:{site}"
    brave = BraveSearch.from_api_key(api_key=settings.BRAVE_SEARCH_API_KEY)
    return brave.run(full_query)


if __name__ == "__main__":
    print(site_specific_search.invoke({"query": "What is the future of AI?", "site": "blog.samaltman.com"}))







    








