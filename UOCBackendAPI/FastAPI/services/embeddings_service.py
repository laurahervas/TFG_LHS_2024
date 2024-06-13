import os
from db.models.embedding import Embedding
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer
from domain.models.log import Log
from services.logger import Logger

class EmbeddingsService:
    
    def __init__(self):
        self.model = os.getenv("EMBEDDING_MODEL")
        self.version = os.getenv("EMBEDDING_VERSION")
        self.modelPath = os.getenv("EMBEDDING_MODEL_PATH")
        self.logger = Logger()

    def execute(self, docs: list[str]) -> list[float]:
        self.logger.debug(
            Log(
                title="Going to generate embeddings",
                file=__name__,
                funcname="execute",
                request=docs,
            )
        )
        model = SentenceTransformer(self.modelPath)
        embeddings = model.encode(docs, convert_to_tensor=False)
        self.logger.debug(
            Log(
                title="Response from generating embeddings",
                file=__name__,
                funcname="execute",
                request=docs,
                response="Ok"
            )
        )
        return embeddings


    
