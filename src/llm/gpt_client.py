from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

import os
load_dotenv()

# use OpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
)
print("gpt_client llm =", llm)