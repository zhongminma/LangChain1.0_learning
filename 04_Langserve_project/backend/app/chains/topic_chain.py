from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from llm import llm
from app.schemas.output import TopicSummary

parser = PydanticOutputParser(pydantic_object=TopicSummary)

prompt = PromptTemplate(
    template="""
You are a technical expert.

{format_instructions}

Topic: {topic}
""",
    input_variables=["topic"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | llm | parser
