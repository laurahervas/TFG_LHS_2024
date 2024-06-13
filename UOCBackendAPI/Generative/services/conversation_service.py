from fastapi import Depends
from services.logger import Logger
from domain.models.log import Log
import json
import os

from services.handle_request import HandleRequest
from domain.models.conversation_response import ConversationResponse


class ConversationService:
    def __init__(
        self,
    ):
        self.handle_request = HandleRequest()
        self.baseUrl = os.getenv("MS_CONVERSATION_URL")
        self.logger = Logger()

    def findConversation(self, conversation_id: str) -> ConversationResponse:
        url = f"{self.baseUrl}/{conversation_id}"
        self.logger.debug(
            Log(
                title="Going to call FastAPI for conversation",
                file=__name__,
                convesation_id=conversation_id,
                funcname="findConversation",
                request=url,
            )
        )
        response = self.handle_request.get(
            url=url,
            params={"conversation": conversation_id}
        )
        self.logger.debug(
            Log(
                title="Response from FastAPI for find conversation",
                file=__name__,
                convesation_id=conversation_id,
                funcname="findConversation",
                request=url,
                response=response.text,
            )
        )
        return ConversationResponse(response.text)
    
    def createConversation(self, user: str, query: str) -> ConversationResponse:
        url = f"{self.baseUrl}/"
        self.logger.debug(
            Log(
                title="Going to call FastAPI for create conversation",
                user_query=query,
                user_id=user,
                file=__name__,
                funcname="createConversation",
                request=url,
            )
        )
        response = self.handle_request.post(
            url=url,
            body=json.dumps({"user": user, "conversation": [{"query": query, "response": ""}]})
        )
        self.logger.debug(
            Log(
                title="Response from FastAPI for create conversation",
                user_query=query,
                user_id=user,
                file=__name__,
                funcname="createConversation",
                request=url,
                response=response.text,
            )
        )
        return ConversationResponse(response.text)
    
    def updateConversation (self, id:id, user: str, query: str, answer: str) -> ConversationResponse:
        url = f"{self.baseUrl}/"
        body = json.dumps({"id":id, "user": user, "conversation": [{"query": query, "response": answer}]})
        self.logger.debug(
            Log(
                title="Going to call FastAPI for create conversation",
                user_query=query,
                user_id=user,
                file=__name__,
                funcname="updateConversation",
                request=body,
            )
        )
        body = json.dumps({"id":id, "user": user, "conversation": [{"query": query, "response": answer}]})
        response = self.handle_request.put(
            url=url,
            body=body
        )

        self.logger.debug(
            Log(
                title="Response from FastAPI for updating conversation",
                user_query=query,
                user_id=user,
                file=__name__,
                funcname="updateConversation",
                request=body,
                response=response.text,
            )
        )
        return ConversationResponse(response.text)