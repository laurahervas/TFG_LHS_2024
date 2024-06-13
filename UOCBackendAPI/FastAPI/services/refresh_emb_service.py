from fastapi import Depends
import pandas as pd
from db.models.embedding import Embedding
from services.search_docs_service import SearchDocService
import os
from services.logger import Logger
from domain.models.log import Log


class RefreshEmbeddings:
    def __init__(self):
        self.logger = Logger()

    def execute(self) -> list[Embedding]:
        SearchDocService.embedddingsList = []
        embedding = os.getenv("EMBEDDING_PKL")
        self.logger.debug(
            Log(
                title="Refresh embedding from",
                file=__name__,
                funcname="execute",
                request=embedding,
            )
        )
        #load the embeddings from the pickle file
        embeddingPickle = pd.read_pickle(embedding)
        lines = embeddingPickle
        self.logger.debug(
            Log(
                title="loaded embedding from file",
                file=__name__,
                funcname="execute",
                request="Ok",
            )
        )

        for index, row in lines.iterrows():
            code = row['CODIGO_FAQ']
            embedding = row['embeddings']
            motivo = row['motivo']
            if pd.isnull(motivo):
                motivo = ""
            else:
                motivo = str(int(motivo))
            newEmbed = Embedding(code=code, embeddings=embedding.tolist(), motivo=motivo)
            SearchDocService.embedddingsList.append(newEmbed)
        self.logger.info(
            Log(
                title="Loaded embeddings in memory successfully",
                file=__name__,
                funcname="execute",
                request="Ok",
            )
        )
        return SearchDocService.embedddingsList
    
    def delete(self):
        SearchDocService.embedddingsList = []
        self.logger.info(
            Log(
                title="Deleting embeddings",
                file=__name__,
                funcname="delete",
                response=SearchDocService.embedddingsList,
            )
        )
        