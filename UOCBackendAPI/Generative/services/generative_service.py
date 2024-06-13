import os
from openai import OpenAI
from services.handle_request import HandleRequest
from services.logger import Logger
from domain.models.log import Log

class GenerativeService:
    def __init__(
        self,
    ):
        self.handle_request = HandleRequest()
        self.baseUrl = os.getenv("MS_GENERATIVE_URL")
        self.api_key = os.getenv("MS_GENERATIVE_APIKEY")
        self.model = os.getenv("MS_GENERATIVE_MODEL")
        self.temp = float(os.getenv("MS_GENERATIVE_TEMP"))
        self.logger = Logger()


    def generative(self, prompt: str, user_query: str):
        url = f"{self.baseUrl}"
      
        params = f"url={url}, model={self.model} with temp={self.temp} and prompt={prompt} and user_query={user_query}"
        self.logger.debug(
            Log(
                user_query=user_query,
                title="Calling model",
                file=__name__,
                funcname="generative",
                request=params,
            )
        )
        client = OpenAI(base_url=url, api_key=self.api_key)
        try:
            completion = client.chat.completions.create(
                model=self.model,
                messages=prompt,
                temperature=self.temp,
                stream=False,
            )
            if len(completion.choices) > 0:
                response = completion.choices[0].message.content
            else:
                response = "No response from generative service"
            
            self.logger.debug(
                Log(
                    user_query=user_query,
                    title="Response from calling model",
                    file=__name__,
                    funcname="generative",
                    request=params,
                    response=response,
                )
            )

        except Exception as e:
            response = f"Exception in generative service: {e}"
            self.logger.error(
                Log(
                    user_query=user_query,
                    title="Calling model",
                    file=__name__,
                    funcname="generative",
                    response=response,
                )
            )
        return completion
