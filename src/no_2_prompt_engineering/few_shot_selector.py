from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_openai import OpenAIEmbeddings
from llm import llm

example_prompt = PromptTemplate.from_template(
    "Input: {input} \n Output: {output}",
)
examples = [
    {"input": "I love this product, it's amazing!", "output": "positive"},
    {"input": "This is the worst service I have ever had.", "output": "negative"},
    {"input": "It's okay, nothing special.", "output": "neutral"},
    {"input": "The app works fine, but the UI feels outdated.","output": "neutral"},
    {"input": "I waited for two hours and nobody showed up.","output": "negative"
    },
]
selector = SemanticSimilarityExampleSelector.from_examples(
    examples = examples,
    embeddings=OpenAIEmbeddings(),
    vectorstore_cls=FAISS,
    k=2
)
prompt = FewShotPromptTemplate(
    example_selector=selector,
    example_prompt=example_prompt,
    suffix= "Input: {input} \n Output:",
    input_variables=['input']
)
chain = prompt | llm
result = chain.invoke({'input': 'I really like this one.'})
print(result.content)


