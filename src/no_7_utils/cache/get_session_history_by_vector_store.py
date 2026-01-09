from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
docs = [
    "User prefers answers in Chinese for faster understanding.",
    "Project uses LangChain 1.x with RunnableWithMessageHistory and session_id.",
    "Backend is FastAPI + LangServe; memory store can be Redis/SQLite/InMemory."
]
vectorstore = FAISS.from_texts(docs, embedding=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use the context if relevant.\n\nContext:\n{context}"),
    ("human", "{question}")
])
chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm | StrOutputParser()
)

print(chain.invoke("我们项目里 session_id 报错 Missing keys 是怎么回事？"))
