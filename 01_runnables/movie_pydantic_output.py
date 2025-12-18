from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from llm import llm

class Movie(BaseModel):
    title: str
    year: str
    director: str
    ratings: str

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = PromptTemplate(
    template="""
    You are a movie expert.
    {format_instructions}
    Movie: {movie_name}
    """,
    input_variables=["movie_name"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | llm | parser

response = chain.invoke({"movie_name": "ZooTopia"})
print(response)
print(type(response))
