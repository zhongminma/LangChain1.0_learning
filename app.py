from langchain_core.prompts import PromptTemplate
from langserve import add_routes
from llm import llm
from fastapi import FastAPI

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple terms"
)
chain = prompt | llm
app = FastAPI(
    title="LangServe Demo",
    version="1.0",
    description="Simple LangChain Server"
)

add_routes(app, chain, path="/explain")
# add_routes(app, gemini_chain, path="/openai")
# add_routes(app, gemini_chain, path="/gemini")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
# pip install langchain langchain-openai fastapi langserve uvicorn
# http://127.0.0.1:8000/docs for swagger
# http://127.0.0.1:8000/explain/playground/ for web ui