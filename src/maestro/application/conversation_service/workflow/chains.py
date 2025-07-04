from ....config import settings

from ....domain.prompts import (
    TEACHER_CHARACTER_CARD,
    EXTEND_SUMMARY_PROMPT,
    SUMMARY_PROMPT,
    SHOULD_BRAVE_SEARCH_PROMPT,
)

from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from ....domain.prompts import BRAVE_SEARCH_PROMPT
from ....application.conversation_service.workflow.tools import retriever_tool, brave_search_tool
from langchain_google_genai import ChatGoogleGenerativeAI



def get_chat_model(model_name: str = settings.GOOGLE_MODEL, temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, api_key=settings.GOOGLE_API_KEY)

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
    model = get_chat_model(settings.GOOGLE_SUMMARY_MODEL)
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



