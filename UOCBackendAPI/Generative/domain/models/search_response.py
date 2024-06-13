import json

from domain.models.document import Document

class SearchResponse:
    def __init__(self, responseText: str):
        self.responseText = responseText
        self.parsedResponse = json.loads(responseText)

    @property
    def documents(self) -> list[Document]:
        if self.parsedResponse.get('documents') is not None:
            return [
                Document(document["code"], document["similarity"])
                for document in self.parsedResponse["documents"]
            ]
        else:
            return [ ]
        
    @property
    def documentsLists(self) -> list[dict]:
        if self.parsedResponse.get('documents') is not None:
            return [
                {"code": document["code"], "similarity": document["similarity"]}
                for document in self.parsedResponse["documents"]
            ]
        else:
            return []