from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from maestro.application.conversation_service.generate_response import get_response
from maestro.domain.teacher_factory import TeacherFactory
from .reset_conversation import reset_conversation_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the API."""
    # Startup code (if any) goes here
    yield
    # Shutdown code goes here


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str
    teacher_id: str


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        teacher_factory = TeacherFactory()
        teacher = teacher_factory.get_teacher(chat_message.teacher_id)

        response, _ = await get_response(
            messages=chat_message.message,
            teacher_id=chat_message.teacher_id,
            teacher_name=teacher.name,
            teacher_perspective=teacher.perspective,
            teacher_style=teacher.style,
            teacher_expertise=teacher.expertise,
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/reset-memory")
async def reset_conversation():
    """Resets the conversation state. It deletes the two collections needed for keeping LangGraph state in MongoDB.

    Raises:
        HTTPException: If there is an error resetting the conversation state.
    Returns:
        dict: A dictionary containing the result of the reset operation.
    """
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
