from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from maestro.application.conversation_service.workflow.edges import (
    should_summarize_conversation,
    should_brave_search,
)
from maestro.application.conversation_service.workflow.nodes import (
    conversation_node,
    summarize_conversation_node,
    brave_search_node,
    summarize_check_node,
)
from langchain_core.messages import HumanMessage
from maestro.domain.teacher_factory import TeacherFactory
from maestro.application.conversation_service.workflow.state import TeacherState, state_to_str


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(TeacherState)

    # Add nodes
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("brave_search_node", brave_search_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    graph_builder.add_node("summarize_check_node", summarize_check_node)  # ← New dummy node

    # Flow
    graph_builder.add_edge(START, "conversation_node")

    # Step 1: from conversation, decide whether to do brave search
    graph_builder.add_conditional_edges(
        "conversation_node",
        should_brave_search,  # returns "brave_search_node" or "summarize_check_node"
        {
            "brave_search_node": "brave_search_node",
            "summarize_check_node": "summarize_check_node",
        },
    )

    # Step 2: brave search → summarize check
    graph_builder.add_edge("brave_search_node", "summarize_check_node")

    # Step 3: from summarize_check_node, conditionally summarize
    graph_builder.add_conditional_edges(
        "summarize_check_node",
        should_summarize_conversation,  # returns "summarize_conversation_node" or "end"
        {
            "summarize_conversation_node": "summarize_conversation_node",
            "end": END,
        },
    )

    # Step 4: summarization ends the graph
    graph_builder.add_edge("summarize_conversation_node", END)

    return graph_builder


# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()

import asyncio

async def main():
    compiled_graph = create_workflow_graph().compile()

    teacher = TeacherFactory.get_teacher("karpathy")

    input_state = {
        "messages": [HumanMessage(content="What is the capital of France?")],
        "teacher_name": teacher.name,
        "teacher_perspective": teacher.perspective,
        "teacher_style": teacher.style,
        "teacher_expertise": teacher.expertise,
        "summary": "",
    }

    final_state = await compiled_graph.ainvoke(TeacherState(**input_state))
    print("Final state:")
    print(final_state)
    
if __name__ == "__main__":
    asyncio.run(main())