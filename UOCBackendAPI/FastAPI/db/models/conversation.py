from pydantic import BaseModel
from typing import Optional

class Conversation(BaseModel):
    id: Optional[str] = None
    user: str
    conversation:list[dict]