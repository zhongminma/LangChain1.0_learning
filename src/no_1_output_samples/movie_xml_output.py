from typing import Any

from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, model_validator

from llm import llm

class Movie(BaseModel):
    title: str
    year: str
    director: str
    ratings: str
    @model_validator(mode='before')
    @classmethod
    def normalized_xml(cls, obj: Any) -> Any:
        if isinstance(obj, dict) and 'movie' in obj:
            obj = obj['movie']
        if isinstance(obj, list):
            merged = {}
            for item in obj:
                if isinstance(item, dict):
                    merged.update(item)
            return merged
        return obj


parser = XMLOutputParser(tags=["movie"])

prompt = PromptTemplate(
    template="""
        You are a movie expert.
        Return ONLY valid XML. No extra text.
        <movie>
          <title>{movie_name}</title>
          <year></year>
          <director></director>
          <ratings></ratings>
        </movie>
    """,
    input_variables=["movie_name"],
)

chain = prompt | llm | parser
xml_dict = chain.invoke({"movie_name": "ZooTopia"})
print(xml_dict)

movie_dict = xml_dict["movie"]
print(movie_dict)

movie = Movie.model_validate(movie_dict)
print(movie)