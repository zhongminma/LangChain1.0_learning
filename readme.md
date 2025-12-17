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

### Use GOOGLE free tier 
pip install google-genai

## 2. test this runnable py
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