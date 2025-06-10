from pydantic import BaseModel, HttpUrl

class KBUrlInput(BaseModel):
    url: HttpUrl

class QueryInput(BaseModel):
    question: str
    knowledge_only: bool = True
