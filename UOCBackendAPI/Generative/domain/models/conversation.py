class Conversation:
    def __init__(
            self,
            id: str,
            user: str,
            query: str, 
            response: str,
        ):
        self.id = id,
        self.user = user,
        self.query = query,
        self.response = response

    def toDict(self):
        return {
            "id": self.id,
            "user": self.user,
            "query": self.query,
            "response": self.response  
        }