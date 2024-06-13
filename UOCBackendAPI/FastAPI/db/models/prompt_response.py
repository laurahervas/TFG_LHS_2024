from pydantic import BaseModel

class PromptResponse(BaseModel):
    prompt: list[dict]