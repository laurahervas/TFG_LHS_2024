from domain.models.document import Document
from pydantic import BaseModel

class SearchDocsResponse(BaseModel):
    documents: list[dict]
