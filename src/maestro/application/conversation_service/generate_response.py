import uuid
from typing import Any, AsyncGenerator, Union, Sequence

from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.mongodb.aio import AsyncMongoDBSaver
from opik.integrations.langchain import OpikTracer

from maestro.application.conversation_service.workflow.graph import create_workflow_graph
from maestro.application.conversation_service.workflow.state import TeacherState
from maestro.config import settings


async def get_response(
    messages: Union[str, list[dict[str, Any]]],
    teacher_id: str,
    teacher_name: str,
    teacher_perspective: str,
    teacher_style: str,
    teacher_expertise: list[str],
    new_thread: bool = False,
) -> tuple[str, TeacherState]:
    """Run a conversation through the workflow graph.

    Args:
        message: Initial message to start the conversation.
        teacher_id: Unique identifier for the teacher.
        teacher_name: Name of the teacher.
        teacher_perspective: Teacher's perspective on the topic.
        teacher_style: Teaching style (e.g., "Socratic").
        teacher_expertise: List of subjects the teacher is expert in.

    Returns:
        tuple[str, TeacherState]: A tuple containing:
            - The content of the last message in the conversation.
            - The final TeacherState.

    Raises:
        RuntimeError: If there's an error running the conversation workflow.
    """

    graph_builder = create_workflow_graph()

    try:
        async with AsyncMongoDBSaver.from_conn_string(
            conn_string=settings.MONGO_URI,
            db_name=settings.MONGO_DB_NAME,
            checkpoint_collection_name=settings.MONGO_STATE_CHECKPOINT_COLLECTION,
            writes_collection_name=settings.MONGO_STATE_WRITES_COLLECTION,
        ) as checkpointer:
            graph = graph_builder.compile(checkpointer=checkpointer)
            opik_tracer = OpikTracer(graph=graph.get_graph(xray=True))

            thread_id = teacher_id if not new_thread else f"{teacher_id}-{uuid.uuid4()}"
            config: RunnableConfig = {
                "configurable": {"thread_id": thread_id},
                "callbacks": [opik_tracer],
            }
            output_state = await graph.ainvoke(
                input={
                    "messages": list(__format_messages(messages=messages)),
                    "teacher_name": teacher_name,
                    "teacher_perspective": teacher_perspective,
                    "teacher_style": teacher_style,
                    "teacher_expertise": teacher_expertise,
                    "summary": "",  # Initialize with empty summary
                },
                config=config,
            )
        last_message = output_state["messages"][-1]
        return last_message.content, TeacherState(**output_state)
    except Exception as e:
        raise RuntimeError(f"Error running conversation workflow: {str(e)}") from e





def __format_messages(
    messages: Union[str, list],
) -> Sequence[Union[HumanMessage, AIMessage]]:
    """Convert various message formats to a list of LangChain message objects.

    Args:
        messages: Can be one of:
            - A single string message
            - A list of string messages
            - A list of dictionaries with 'role' and 'content' keys

    Returns:
        List[Union[HumanMessage, AIMessage]]: A list of LangChain message objects
    """

    if isinstance(messages, str):
        return [HumanMessage(content=messages)]

    if isinstance(messages, Sequence):
        if not messages:
            return []

        if (
            isinstance(messages[0], dict)
            and "role" in messages[0]
            and "content" in messages[0]
        ):
            result = []
            for msg in messages:
                if msg["role"] == "user":
                    result.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    result.append(AIMessage(content=msg["content"]))
            return result

        return [HumanMessage(content=message) for message in messages]

    return []
