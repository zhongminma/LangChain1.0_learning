from langchain_core.prompts import PromptTemplate
from llm import llm

str_prompts = PromptTemplate.from_template('Tell me a joke about {topic}')
chain = str_prompts | llm
result = chain.invoke({'topic': 'dog'})
print(result)
print(result.content)
