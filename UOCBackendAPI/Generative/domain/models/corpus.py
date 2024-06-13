from uuid import UUID

class Corpus:
    def __init__(
            self, 
            id: str,
            code: str,
            texto: str, 
            title: str, 
            variaciones: str,
            motivo:int,
            tokens: int
        ):
        self.id = id
        self.code = code
        self.texto = texto
        self.title = title
        self.variaciones = variaciones
        self.motivo = motivo
        self.tokens = tokens


    def toDict(self):
        return {
            "id": self.id, 
            "code": self.code, 
            "texto": self.texto,
            "title": self.title, 
            "variaciones": self.variaciones,
            "motivo": self.motivo,
            "tokens": self.tokens, 
        }

