from fastapi import Depends

import os

from domain.models.prompt_response import PromptResponse
from domain.models.prompt import Prompt
from services.handle_request import HandleRequest
from services.logger import Logger
from domain.models.log import Log

class PromptService:
    def __init__(
        self,
    ):
        self.handle_request = HandleRequest()
        self.baseUrl = os.getenv("MS_PROMPT_URL")
        self.logger = Logger()
      
    def getPrompt(self, code:str) -> Prompt:
        url = f"{self.baseUrl}/code/{code}"
        self.logger.debug(
            Log(
                title="Going to call FastAPI for prompt",
                file=__name__,
                funcname="getPrompt",
                request=url,
            )
        )
        response = self.handle_request.get(
            url=url,
            params={}
        )
        self.logger.debug(
            Log(
                title="Response from FastAPI for prompt",
                file=__name__,
                funcname="getPrompt",
                request=url,
                response=response.text,
            )
        )
        return PromptResponse(response.text)