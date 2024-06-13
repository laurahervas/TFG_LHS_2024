from pydantic import BaseModel
from typing import Optional

class Prompt(BaseModel):
    id: Optional[str] = None
    code:int
    name: str
    prompt:str
