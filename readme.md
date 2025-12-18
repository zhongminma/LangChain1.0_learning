# follow LangChain v1.0 docs and setup env

## 1. Installation
1. install langchain
2. install openAI and anthropic
3. install dotenv (for API Keys)

## 2. env and API Keys
1. create a file .env and add keys
2. check LangChain integrations to find llm providers
3. API_KEYS from https://aistudio.google.com/api-keys
4. BASE_URL is https://generativelanguage.googleapis.com

#### pip install package
1. Use GOOGLE free tier 
pip install google-genai
2. Use GOOGLE free tier 
pip install openai, python-dotenv

## 3. test this runnable py
#### check LLM provider for documentation and runnable helloworld code

## using Gemini free tier
```python
from google import genai
from langchain_core.runnables import RunnableLambda
client = genai.Client()
def gemini_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt
    )
    return response.text
llm = RunnableLambda(gemini_llm)

print(llm.invoke("Respond with OK only"))
print(llm.invoke("when gemini release year"))
```

## Using OpenAI API Keys
```python
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
response = llm.invoke("Say OK Open AI")
print(response.content)
```