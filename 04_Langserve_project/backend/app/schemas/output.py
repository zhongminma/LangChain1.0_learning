from pydantic import BaseModel

class TopicSummary(BaseModel):
    title: str
    summary: str
    pros: list[str]
    cons: list[str]
