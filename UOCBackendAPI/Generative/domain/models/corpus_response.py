import json

from domain.models.corpus import Corpus

class CorpusResponse:
    def __init__(self, responseText: str):
        self.responseText = responseText
        self.parsedResponse = json.loads(responseText)

    @property
    def corpus(self) -> Corpus:
        if self.parsedResponse is not None:
            id=self.parsedResponse["id"],
            code=self.parsedResponse["code"],
            texto=self.parsedResponse["texto"],
            title=self.parsedResponse["title"],
            variaciones=self.parsedResponse["variaciones"],
            motivo=self.parsedResponse["motivo"],
            num_tokens=int(self.parsedResponse["num_tokens"])
        
            return Corpus(id,code,texto,title,variaciones,motivo,num_tokens)
            
        else:
            return None
        
    @property
    def corpusList(self) -> list[dict]:
        if self.parsedResponse is not None:
            return [
                {"code":corpus["code"],"texto":corpus["texto"], "title":corpus["title"],"variaciones":corpus["variaciones"], "motivo":corpus["motivo"],"num_tokens":corpus["num_tokens"]}
                for corpus in self.parsedResponse["corpus"]
            ]
        else:
            return []