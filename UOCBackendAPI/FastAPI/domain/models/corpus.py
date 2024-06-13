class Corpus:
    def __init__(
            self, 
            id: str,
            code: int,
            title: str, 
            texto: str,
            variaciones: str,
            num_variaciones: int,
            motivo: str,
            intent: str, 
            num_tokens: int 
        ):
        self.id = id
        self.code = code
        self.title = title
        self.texto = texto
        self.variaciones = variaciones
        self.num_variaciones = num_variaciones
        self.motivo = motivo
        self.intent = intent
        self.num_tokens = num_tokens

    def toDict(self):
        return {
            "id": self.id, 
            "code": self.code,
            "title": self.title,
            "texto": self.texto,
            "variaciones": self.variaciones,
            "num_variaciones": self.num_variaciones,
            "motivo": self.motivo,
            "intent": self.intent,
            "num_tokens": self.num_tokens
            
        }