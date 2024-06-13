
from pydantic import BaseModel
from typing import Optional

class Document(BaseModel):
    code:str
    similarity:float