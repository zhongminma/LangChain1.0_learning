from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel
from llm import llm

class Movie (BaseModel):
    title: str
    year: str
    director: str
    ratings: str

# parser
movie_parser = JsonOutputParser()

# prompt
prompt = PromptTemplate(
    template="""
    You are a movie expert.
    Return the answer in valid JSON ONLY.
    Do not include any extra text, markdown, or explanations.
    {{
        "title": "string",
        "year": "string",
        "director": "string",
        "ratings": "string"
    }}
        Movie: {movie_name}
    """,
    input_variables=["movie_name"],
)
# chain
chain = prompt | llm | movie_parser

# call
response = chain.invoke({"movie_name": 'ZooTopia'})
print(response)
print(type(response))