from fastapi import Depends
from services.logger import Logger
from domain.models.log import Log
import os

from services.handle_request import HandleRequest
from domain.models.search_response import SearchResponse

class SearchService:
    def __init__(
        self,
    ):
        self.handle_request = HandleRequest()
        self.baseUrl = os.getenv("MS_SEARCH_URL")
        self.logger = Logger()

    def search(self, user_query: str) -> SearchResponse:
        url = f"{self.baseUrl}/search"
        self.logger.debug(
            Log(
                title="Going to call FastAPI for search",
                file=__name__,
                user_query=user_query,
                funcname="search",
                request=url,
            )
        )
        response = self.handle_request.get(
            url=url,
            params={"user_query": user_query}
        )
        
        responseText = (response.text, {"documents":[]})[response == None]
        self.logger.debug(
            Log(
                title="Response from FastAPI for search",
                file=__name__,
                user_query=user_query,
                funcname="search",
                request=url,
                response=responseText,
            )
        )
        
        return SearchResponse(responseText)