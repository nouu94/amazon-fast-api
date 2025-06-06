from pydantic import BaseModel

class SearchRequest(BaseModel):
    Keywords: str