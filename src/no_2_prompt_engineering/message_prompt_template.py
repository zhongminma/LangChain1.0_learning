from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ('system', 'you are a helpful assistant'),
    MessagesPlaceholder('msg')
])
result = prompt.invoke({'msg': [HumanMessage(content='Hi'), HumanMessage(content='Aloha')]})
print(result)