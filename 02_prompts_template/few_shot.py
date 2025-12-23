from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from llm import llm

example_prompt = PromptTemplate.from_template(
    "Input: {input}\nOutput: {output}"
)
examples = [
    {'input': 'dog', 'output':'A hunting related animal'},
    {'input': 'horse', 'output':'A transportation related animal'}
]
prompt = FewShotPromptTemplate(
    examples = examples,
    example_prompt=example_prompt,
    suffix="Input: {input}\nOutput:", input_variables=['input']
)
chain = prompt | llm
result = chain.invoke({'input': 'cat'})
print(result.content)