from fastapi import FastAPI
from app.routes import chat, health
from app.routes import debug
from app.storage.vector_store import init_collection

app = FastAPI(title="RAG API")

@app.on_event("startup")
def startup_event():
    init_collection()

app.include_router(chat.router)
app.include_router(health.router)
app.include_router(debug.router)