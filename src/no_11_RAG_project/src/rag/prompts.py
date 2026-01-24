from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Use ONLY the provided context. If not in context, say you don't know."),
        ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
    ]
)
