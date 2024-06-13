### User model ###

from pydantic import BaseModel
from typing import Optional

from db.models.conversation import Conversation

#id: Optional[str] 
#id: str | None

class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: str
    conversation: list[Conversation]
