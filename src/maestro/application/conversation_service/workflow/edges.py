from maestro.application.conversation_service.workflow.chains import  get_should_brave_search_chain
from ....config import settings
from maestro.application.conversation_service.workflow.state import TeacherState
from typing_extensions import Literal
from langchain_core.messages import HumanMessage


def should_summarize_conversation(
    state: TeacherState,
) -> Literal["summarize_conversation_node", "end"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"
    return "end"


# The StateGraph supports async conditional functions, so we make this async
# to leverage the async LLM chain.

async def should_brave_search(
    state: TeacherState,
) -> Literal["brave_search_node", "summarize_check_node"]:
    """Decide whether we should invoke the Brave Search branch.

    We ask the `get_should_brave_search_chain` LLM whether to perform an
    external search based on the **last user message**.
    The chain is expected to reply with either
    "brave_search_node" (perform search) or any other value meaning no search.
    """
    # Find the most recent user (Human) message; Gemini requires requests to end with a user role
    # If no user message is found, skip the Brave search branch.
    last_message = next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        None,
    )

    if last_message is None:
        return "summarize_check_node"

    chain = get_should_brave_search_chain()

    # Call the async variant so we don't block the event loop
    response = await chain.ainvoke({"messages": [last_message]})

    decision = str(response.content).strip()
    if decision == "brave_search_node":
        return "brave_search_node"

    return "summarize_check_node"



