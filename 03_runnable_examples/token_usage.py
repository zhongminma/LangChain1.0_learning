from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI

from llm import llm
response = llm.invoke('hello')
print(response.response_metadata)  # get prompt,total,completion attr name
print(response.response_metadata['token_usage'])

class TokenUsageCallback(BaseCallbackHandler):
    def __init__(self):
        self.prompt_token = 0
        self.completion_token = 0
        self.total_tokens = 0

callback = TokenUsageCallback()
llm_usage = ChatOpenAI(
    model="gpt-4o-mini",
    callbacks = [callback]
)
res = llm_usage.invoke('Explain LangChain Token usage')
print(res.response_metadata['token_usage'])
