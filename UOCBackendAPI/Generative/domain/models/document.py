class Document:
    def __init__(self, code: str, similarity: float):
        self.code = code 
        self.similarity = similarity
    def __str__(self):
        return f"'code':{self.code}, 'similarity'={self.similarity}"