from pydantic import BaseModel
from llm import llm

class Movie(BaseModel):
    title: str
    year: str
    director: str
    ratings: str

structured_llm = llm.with_structured_output(Movie)

response = structured_llm.invoke("Provide information about the movie ZooTopia")
print(response)
print(type(response))
