from langgraph.graph import MessagesState


class TeacherState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information
    necessary to maintain a coherent conversation between the Teacher persona
    and the user.

    Attributes:
        teacher_context (str): The historical and domain context of the teacher.
        teacher_name (str): The name of the teacher.
        teacher_perspective (str): The perspective of the teacher on the subject.
        teacher_style (str): The characteristic teaching style of the teacher.
        summary (str): A running summary of the conversation used to reduce token
            usage.
    """


    # Persona information
    teacher_name: str
    teacher_perspective: str
    teacher_style: str
    teacher_expertise: list[str]
    # Conversation tracking
    summary: str


def state_to_str(state: "TeacherState") -> str:  
    """Return a readable string representation of the state for debugging."""
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return (
        "TeacherState("
        f"teacher_name={state['teacher_name']}, "
        f"teacher_perspective={state['teacher_perspective']}, "
        f"teacher_style={state['teacher_style']}, "
        f"conversation={conversation})"
    )
