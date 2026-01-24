# LangChain RAG Notes

RAG stands for Retrieval-Augmented Generation. It combines retrieval of external knowledge with LLM generation.

Key steps:
1) Load documents
2) Split into chunks
3) Embed chunks
4) Store in vector database
5) Retrieve top-k chunks for a query
6) Generate answer grounded in retrieved context
