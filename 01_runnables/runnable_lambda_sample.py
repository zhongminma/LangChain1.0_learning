from langchain_core.runnables import RunnableLambda
from llm import gemini_llm

#
llm = RunnableLambda(gemini_llm)
print(llm.invoke("Respond with OK only"))
print(llm.invoke("when gemini release year"))