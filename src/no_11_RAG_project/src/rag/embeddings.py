from langchain_openai import OpenAIEmbeddings

def build_embeddings(model: str) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=model)
