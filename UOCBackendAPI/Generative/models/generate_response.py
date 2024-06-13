from pydantic import BaseModel

class GenerateResponse(BaseModel):
    answer: str
    tokens: int



