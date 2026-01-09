import uuid

from dotenv import load_dotenv
from starlette.requests import Request
from starlette.responses import Response

load_dotenv()
from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware
from app.chains.topic_chain import chain as topic_chain
from app.chains.chat_chain_redis import chat_chain_redis
from app.chains.conversation_chain import build_chain

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

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # 允许前端传，也允许后端兜底生成
    rid = request.headers.get("x-request-id") or str(uuid.uuid4())

    response: Response = await call_next(request)

    # 回传给前端：Network/Console 一眼能看到
    response.headers["x-request-id"] = rid
    return response

add_routes(
    app,
    topic_chain,
    path="/api/llm",
    config_keys=["metadata", "tags"]
)

# add_routes(app, chat_chain_session, path="/api/chat")
add_routes(app, chat_chain_redis, path="/api/chat_redis")
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
async def chat(payload: dict):
    user_id = payload["user_id"]
    conversation_id = payload["conversation_id"]
    input_text = payload["input"]

    chain = build_chain(user_id, conversation_id)
    session_id = f"{user_id}:{conversation_id}"
    config = {
        "configurable": {"session_id": session_id},
        "tags": ["api", "chat"],
        "metadata": {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "session_id": session_id,
        },
    }

    result = await chain.ainvoke({"input": input_text}, config=config)
    return {"output": result.content}
