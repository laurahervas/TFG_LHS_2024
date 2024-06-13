import json

from domain.models.prompt import Prompt

class PromptResponse:
    def __init__(self, responseText: str):
        self.responseText = responseText
        self.parsedResponse = json.loads(responseText)

    @property
    def prompt(self) -> Prompt:
        if self.parsedResponse is not None:
            id = self.parsedResponse["id"]
            code = self.parsedResponse["code"]
            name = self.parsedResponse["name"]
            prompt = self.parsedResponse["prompt"]
            return Prompt(id, code, name, prompt)
        else:
            return None
        
