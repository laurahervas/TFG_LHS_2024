from typing import Optional
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    conversation: Optional[str] = None
    user: str
    query: str