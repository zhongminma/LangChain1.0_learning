from fastapi import FastAPI
from langserve import add_routes
from starlette.middleware.cors import CORSMiddleware
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

# add_routes(app, chain, path="/api/llm")
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
    result = await chain.ainvoke({"input": input_text})

    return result
