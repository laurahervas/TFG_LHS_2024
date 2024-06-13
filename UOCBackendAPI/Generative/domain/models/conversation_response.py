from domain.models.conversation import Conversation
import json

class ConversationResponse:
    def __init__(self, responseText: str):
        self.responseText = responseText
        self.parsedResponse = json.loads(responseText)

    @property
    def conversation(self) -> Conversation:
        if self.parsedResponse is not None:
            conversation=self.parsedResponse["conversation"],
        
            return Conversation(conversation["query"],conversation["response"])
        else:
            return None
        
    @property
    def conversationList(self) -> list[dict]:
        if self.parsedResponse is not None:
            return [
                {"query":conversation["query"],"response":conversation["response"]}
                for conversation in self.parsedResponse["conversation"]
            ]
        else:
            return []