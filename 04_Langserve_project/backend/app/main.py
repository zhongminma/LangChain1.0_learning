from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware

from app.chains.chat_chain_session import chat_chain_session
from app.chains.chat_chain_redis import chat_chain_redis
from app.chains.topic_chain import chain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add_routes(app, chain, path="/api/llm")
# add_routes(app, chat_chain_session, path="/api/chat")
add_routes(app, chat_chain_redis, path="/api/chat_redis")
@app.get("/health")
def health():
    return {"status": "ok"}

# 启动：
# uvicorn app.main:app --reload
