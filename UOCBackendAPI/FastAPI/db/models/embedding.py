### Embedding model ###

from pydantic import BaseModel
from typing import Optional

#id: Optional[str] 
#id: str | None

class Embedding(BaseModel):
    id: Optional[str] = None
    code:int
    embeddings: list[float]
    motivo:str
