import os

class Log:
    
    def __init__(
        self,
        convesation_id: str = None,
        user_query: str = None,
        file: str = None,
        funcname: str = None,
        title: str = None,
        request: str = None,
        response: str = None,
        user_id: str = None,
    ):
        self.convesation_id = convesation_id or "None"
        self.user_query = user_query or "None"
        self.file = file or "None"
        self.funcname = funcname or "None"
        self.title = title or "None"
        self.request = request or "None"
        self.response = response or "None"
        self.user_id = user_id or "None"

    def getLog(self) -> dict:
        return {
            "convesation_id": self.convesation_id,
            "user_id": self.user_id,
            "file": self.file,
            "funcname": self.funcname,
            "user_query": self.user_query,
            "title": self.title,
            "request": self.request,
            "response": self.response
        }
