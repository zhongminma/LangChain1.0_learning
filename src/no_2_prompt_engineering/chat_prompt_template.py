from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful assistant'),
    ('human', 'tell me a joke about {topic}')
])
result = chat_prompt_template.invoke({'topic': 'dog'})
print(result)
