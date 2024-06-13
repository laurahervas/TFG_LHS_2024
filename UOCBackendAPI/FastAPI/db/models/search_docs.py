from pydantic import BaseModel

class SearchDocs(BaseModel):
    documents: list[dict]