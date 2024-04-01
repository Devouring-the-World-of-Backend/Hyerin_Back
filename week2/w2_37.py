from pydantic import BaseModel

class Book(BaseModel):
    id: int 
    title:str
    author: str | None = None
    description: str | None = None
    published_year: int | None = None
