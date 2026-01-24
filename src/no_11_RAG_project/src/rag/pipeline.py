from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from .prompts import RAG_PROMPT


def build_rag_chain(chat_model: str, retriever):
    llm = ChatOpenAI(model=chat_model)

    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[source: {d.metadata.get('source','unknown')}]\n{d.page_content}"
            for d in docs
        )

    # retriever: Runnable[str, List[Document]]
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain
