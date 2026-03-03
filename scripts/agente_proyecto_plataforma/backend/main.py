from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ChatRequest, ChatResponse
from .agent_router import handle_chat
from .file_router import router as file_router

app = FastAPI(
    title="Plataforma Multiagente de Ciencia de Datos",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = handle_chat(request.message)
    return {"response": response}
