
from langchain_core.runnables import RunnableLambda
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
# auto read from .env
load_dotenv()
# use OpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
)
