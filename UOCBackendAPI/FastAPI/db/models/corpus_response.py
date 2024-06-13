from pydantic import BaseModel

class CorpusDocsResponse(BaseModel):
    corpus: list[dict]