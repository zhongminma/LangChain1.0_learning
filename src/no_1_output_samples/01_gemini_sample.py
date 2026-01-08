import sys
print("SYS.PATH[0:3] =", sys.path[:3])

from langchain_core.runnables import RunnableLambda
from llm.gemini_client import gemini_llm

llm = RunnableLambda(gemini_llm)

print(llm.invoke("Respond with OK"))
print(llm.invoke("When was Gemini released?"))
