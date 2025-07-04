from langchain_ollama import ChatOllama

from ....config import settings
from ....domain.teachers import Teacher

from ....domain.prompts import (
    TEACHER_CHARACTER_CARD,
    EXTEND_SUMMARY_PROMPT,
    SUMMARY_PROMPT,
    SHOULD_BRAVE_SEARCH_PROMPT,
)


from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from ....domain.prompts import BRAVE_SEARCH_PROMPT
from ....application.conversation_service.workflow.tools import retriever_tool, brave_search_tool




def get_chat_model(model_name: str = settings.OLLAMA_MODEL_NAME, temperature: float = 0.7) -> ChatOllama:
    """Return a ChatOllama model from LangChain community wrapper."""
    return ChatOllama(model=model_name, temperature=temperature)


def get_teacher_response_chain():
    model = get_chat_model()
    model = model.bind_tools([retriever_tool])
    system_message = TEACHER_CHARACTER_CARD

    prompt = ChatPromptTemplate.from_messages(
        [
        ("system", system_message.prompt),
        MessagesPlaceholder(variable_name="messages"),
    ],
    )
    return prompt | model 


def get_brave_search_chain():
    model = get_chat_model()
    model = model.bind_tools([brave_search_tool])
    system_message = BRAVE_SEARCH_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            ("system", system_message.prompt),
        ],
    )
    return prompt | model

def get_conversation_summary_chain(summary: str = ""):
    model = get_chat_model(settings.OLLAMA_SUMMARY_MODEL)
    model = model.bind_tools([retriever_tool])
    summary_message = EXTEND_SUMMARY_PROMPT if summary else SUMMARY_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            ("human", summary_message.prompt),
        ],
    )
    
    return prompt | model





def get_should_brave_search_chain():
    model = get_chat_model()
    system_message = SHOULD_BRAVE_SEARCH_PROMPT
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message.prompt),
            MessagesPlaceholder(variable_name="messages"),
        ],
    )
    return prompt | model



