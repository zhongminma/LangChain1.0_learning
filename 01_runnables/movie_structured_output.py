from email.feedparser import boundaryendRE

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.retry import RunnableRetry
from pydantic import BaseModel
from llm import llm

class Movie(BaseModel):
    title: str
    year: str
    director: str
    ratings: str

primary_prompt = PromptTemplate(
    template = """Provide information about the movie ZooTopia"""
)
# include_raw param can provide more info for AIMessage
structured_llm = llm.with_structured_output(Movie, include_raw=True)

primary_chain = primary_prompt | structured_llm


retry_chain = RunnableRetry(
    bound = primary_chain,
    max_attempts= 3,
)
# invalid JSON
fix_prompt = PromptTemplate(
    template = """
    The following output is invalid JSON or does not match the schema.
    Fix it and return ONLY valid JSON.
    Schema: {schema}
    Output: {bad_output}  
    """,
    input_variables= ['bad_output'],
)
fix_chain = fix_prompt | structured_llm

def safe_invoke():
    try:
        return retry_chain.invoke({})
    except Exception as e:
        bad_output  = str(e)
        return fix_chain.invoke({'bad_output': bad_output})
result = safe_invoke()
print(result)
