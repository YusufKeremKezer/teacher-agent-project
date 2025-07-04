from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import RemoveMessage
from ....config import settings
from langchain_community.chat_models import ChatOllama
from maestro.application.conversation_service.workflow.chains import (
get_conversation_summary_chain,
get_teacher_response_chain,
get_brave_search_chain,
get_should_brave_search_chain,
)
from typing_extensions import Literal
from maestro.application.conversation_service.workflow.state import TeacherState
from .tools import (
    retriever_tool,
    brave_search_tool,
)
from langgraph.prebuilt import ToolNode
from maestro.domain.teacher_factory import PERSONAL_SITES


async def summarize_conversation_node(state: TeacherState):
    summary = state.get("summary", "")
    summary_chain = get_conversation_summary_chain(summary)

    response = await summary_chain.ainvoke(
        {
            "messages": state["messages"],
            "teacher_name": state["teacher_name"],
            "summary": summary,
        }
    )

    return {"summary": response.content}


retriever_node = ToolNode([retriever_tool])


async def conversation_node(state: TeacherState):
    summary = state.get("summary", "")
    conversation_chain = get_teacher_response_chain()

    response = await conversation_chain.ainvoke(
        {
            "messages": state["messages"],
            "teacher_name": state["teacher_name"],
            "teacher_perspective": state["teacher_perspective"],
            "teacher_style": state["teacher_style"],
            "teacher_expertise": state["teacher_expertise"],
            "summary": summary,
        },
    )
    
    return {"messages": response}

async def summarize_check_node(state: TeacherState) -> TeacherState:
    return state  # just pass through


async def brave_search_node(state: TeacherState, ):
    summary = state.get("summary", "")
    brave_search_chain = get_brave_search_chain()
    response = await brave_search_chain.ainvoke(
        {
            "messages": state["messages"],
            "summary": summary,
        },
        
    delete_messages = [
        RemoveMessage(id=m.id)
        for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
    ]
    )

    return {"messages": response}




