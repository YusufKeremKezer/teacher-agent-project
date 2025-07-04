from langgraph.graph import END
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from maestro.application.conversation_service.workflow.chains import get_chat_model, get_should_brave_search_chain
from ....domain.prompts import SHOULD_BRAVE_SEARCH_PROMPT
from ....config import settings
from maestro.application.conversation_service.workflow.state import TeacherState
from typing_extensions import Literal


def should_summarize_conversation(
    state: TeacherState,
) -> Literal["summarize_conversation_node", "__END__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"
    return "__END__"


# The StateGraph supports async conditional functions, so we make this async
# to leverage the async LLM chain.

async def should_brave_search(
    state: TeacherState,
) -> Literal["brave_search_node", "__END__"]:
    """Decide whether we should invoke the Brave Search branch.

    We ask the `get_should_brave_search_chain` LLM whether to perform an
    external search based on the **last user message**.
    The chain is expected to reply with either
    "brave_search_node" (perform search) or any other value meaning no search.
    """
    last_message = state["messages"][-1]
    chain = get_should_brave_search_chain()

    # Call the async variant so we don't block the event loop
    response = await chain.ainvoke({"messages": last_message})

    decision = str(response.content).strip()
    if decision == "brave_search_node":
        return "brave_search_node"

    return "__END__"



