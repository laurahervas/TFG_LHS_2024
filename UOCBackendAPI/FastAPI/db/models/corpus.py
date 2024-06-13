
from pydantic import BaseModel
from typing import Optional

class Corpus(BaseModel):
    id: Optional[str] = None
    code:int
    title:str
    texto:str
    variaciones:str
    num_variaciones:int
    motivo:str
    intent:str
    num_tokens:int
