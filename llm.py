from typing import Any
from google import genai
from google.genai import types
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

'''
client = genai.Client()
def gemini_llm(prompt: Any) -> Any:
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=256
        ),
    )
    return response.text
# call runnable
llm = RunnableLambda(gemini_llm)
'''
