import numpy as np
from fastapi import Depends
from services.embeddings_service import EmbeddingsService

import os

from db.models.embedding import Embedding
from domain.models.document import Document
from services.logger import Logger
from domain.models.log import Log

class SearchDocService:
    embedddingsList: list[Embedding] = []

    def __init__(self):
        self.SEARCH_THRESHOLD = float(os.getenv("SEARCH_THRESHOLD"))
        self.SEARCH_MAX_DOCUMENTS = int(os.getenv("SEARCH_MAX_DOCUMENTS"))
        self.embeddingsService = EmbeddingsService()
        self.logger = Logger()


    def find(self, userQuery: str) -> list[Document]:
        self.logger.debug(
            Log(
                title="Going to generate embedding of the user query",
                file=self.__class__.__name__,
                funcname="find",
                request=userQuery,
            )
        )
        queryEmbedding = self.embeddingsService.execute(userQuery)
        self.logger.info(
            Log(
                title="User query embedding generated",
                file=self.__class__.__name__,
                funcname="find",
                request=userQuery,
                response=str(queryEmbedding[0:2]),
            )
        )
        similarities = self._computeSimilarities(userQuery, queryEmbedding)
        self.logger.debug(
            Log(
                title="Compute similarities with the user query embedding",
                file=self.__class__.__name__,
                funcname="find",
                request=str(queryEmbedding[0:2]),
                response=str(similarities)[0:50],
            )
        )
        topDocsText = F"Top {self.SEARCH_MAX_DOCUMENTS} documents, with similarity > {self.SEARCH_THRESHOLD}"
        self.logger.info(
            Log(
                title="Gettings top documents from the similarities",
                file=self.__class__.__name__,
                funcname="find",
                request=str(queryEmbedding[0:2]),
                response=topDocsText,
            )
        )
        topDocs = self._topDocs(
            similarities=similarities,
            threshold=self.SEARCH_THRESHOLD,
            N=self.SEARCH_MAX_DOCUMENTS,
        )
        documents = [
            Document(code=similarity[0], similarity=similarity[1])
            for similarity in topDocs
        ]
        if len(documents) <= 0:
            self.logger.error(
                Log(
                    title="No documents found with similarity > threshold",
                    file=self.__class__.__name__,
                    funcname="find",
                    request=topDocsText,
                    response=documents,
                )
            )
            return []
        
        self.logger.info(
            Log(
                title="Selected documents",
                file=self.__class__.__name__,
                funcname="find",
                request=topDocsText,
                response=documents,
            )
        )
        return documents

    def _computeSimilarities(self, userQuery: str, queryEmbedding: list[float]) -> dict:
        vectors = np.array(
            [embedding.embeddings for embedding in SearchDocService.embedddingsList]
        )
        queryVector = np.array(queryEmbedding)
        similarities = {}
        for i in range(0, len(vectors)):
            embedding = SearchDocService.embedddingsList[i]
            similarity = self._computeCosineSimilarity(queryVector, vectors[i])
            similarity = self._adjustScore(
                similarity=similarity, motivo=embedding.motivo, userQuery=userQuery
            )
            if (
                embedding.code not in similarities
                or similarities[embedding.code] < similarity
            ):
                similarities[embedding.code] = similarity

        return similarities

    def _topDocs(self, similarities: dict, threshold: float, N: int) -> list[tuple]:
        simText = str(similarities)[0:50]    
        topDocsText = F"Docs {simText} max number of {N} documents, with similarity > {threshold}"
        self.logger.debug(
            Log(
                title="Going to select TopDocs",
                file=self.__class__.__name__,
                funcname="_topDocs",
                request=topDocsText,
            )
        )
        if N > len(similarities):
            N = len(similarities)

        sorted = list(similarities.items())
        sorted.sort(key=lambda item: item[1], reverse=True)

        self.logger.debug(
            Log(
                title="Top documents to return",
                file=self.__class__.__name__,
                funcname="_topDocs",
                request=topDocsText,
                response=str(sorted[0:N]),
            )
        )

        for i in range(0, N):
            if sorted[i][1] < threshold:
                return sorted[0:i]
        
        return sorted[0:N]

    def _adjustScore(
        self, similarity: float, motivo: str | None, userQuery: str
    ) -> float:
        if motivo is not None and len(motivo) > 0 and motivo in userQuery:
            reward = 0.05 * (len(motivo) - 1)
        else:
            reward = 0

        return similarity + reward

    def _computeCosineSimilarity(self, a, b):
        cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        return cos_sim
