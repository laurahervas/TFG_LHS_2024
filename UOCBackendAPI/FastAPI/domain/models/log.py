import os

class Log:
    
    def __init__(
        self,
        file: str = None,
        funcname: str = None,
        title: str = None,
        request: str = None,
        response: str = None,
    ):
        self.file = file or "None"
        self.title = title or "None"
        self.funcname = funcname or "None"
        self.request = request or "None"
        self.response = response or "None"

    def getLog(self) -> dict:
        return {
            "file": self.file,
            "funcname": self.funcname,
            "title": self.title,
            "request": self.request,
            "response": self.response
        }
