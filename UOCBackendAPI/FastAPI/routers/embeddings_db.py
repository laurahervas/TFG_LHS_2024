### Users API ###
import json
import pandas as pd
from domain.models.document import Document
from db.models.search_docs_response import SearchDocsResponse
from services.search_docs_service import SearchDocService
from domain.models.user_query import UserQueryStatement
from db.models.search_docs import SearchDocs
from db.models.embedding import Embedding
from db.schemas.embedding import embeddings_schema,embedding_schema
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.client import db_client
from bson import ObjectId
import os
from services.logger import Logger
from domain.models.log import Log

router = APIRouter(prefix="/embeddings",
                   tags=["embeddings"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/", response_model=list[Embedding])
async def embeddings():
    return embeddings_schema(db_client.embedding.find())


@router.post("/", response_model=Embedding, status_code=status.HTTP_201_CREATED)
async def embeding(embedding: Embedding):
    '''
    inserta un nuevo embedding en la base de datos
    @param embedding: Embedding
    '''
    logger = Logger()
    embed_dict = dict(embedding)
    del embed_dict["id"]

    logger.debug(
        Log(
            title="Going to add embedding to DB",
            file=__name__,
            funcname="embeding",
            request=embed_dict,
        )
    )
    id = db_client.embedding.insert_one(embed_dict).inserted_id
    
    #comprobar si el id está en la base de datos
    #el nombre de la clave unica del id es _id
    new_embed = embedding_schema(db_client.embedding.find_one({"_id": id}))
    logger.info(
        Log(
            title="Response from adding embedding to DB",
            file=__name__,
            funcname="embeding",
            request=embed_dict,
            response=new_embed,
        )
    )
    return Embedding(**new_embed)

@router.get("/reload_embeddings", response_model=list[Embedding])
async def reload_embeddings():
    logger = Logger()
    embeddingsList = []
    
    #delete all the embeddings in database
    db_client.embedding.delete_many({})
    corpus_embed = os.getenv("EMBEDDING_PKL")
    embeddingPickle = pd.read_pickle(corpus_embed)
    logger.debug(
        Log(
            title="Reload embedding from",
            file=__name__,
            funcname="reload_embeddings",
            request=corpus_embed,
        )
    )
    lines = embeddingPickle
    
    logger.debug(
        Log(
            title="loaded embedding from file",
            file=__name__,
            funcname="reload_embeddings",
            request=lines,
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
        embeddingsList.append(newEmbed)
        addEmbeddingToDB(newEmbed,logger)
    
    logger.debug(
        Log(
            title="Added embeddings from file to DB",
            file=__name__,
            funcname="reload_embeddings",
            response=embeddingsList,

        )
    )

    return embeddingsList


def addEmbeddingToDB(embedding: Embedding, logger: Logger):
    embed_dict = dict(embedding)
    del embed_dict["id"]
    logger.debug(
        Log(
            title="Going to add embedding to DB",
            file=__name__,
            funcname="addEmbeddingToDB",
            request=embed_dict,
        )
    )
    id = db_client.embedding.insert_one(embed_dict).inserted_id
    logger.debug(
        Log(
            title="Response from adding embedding to DB",
            file=__name__,
            funcname="addEmbeddingToDB",
            request=embed_dict,
            response=id,
        )
    )
    #comprobar si el id está en la base de datos
    #el nombre de la clave unica del id es _id
    new_embed = embedding_schema(db_client.embedding.find_one({"_id": id}))
 
    return Embedding(**new_embed)


@router.get("/search/", response_model=SearchDocsResponse)
async def search( user_query: str):
    logger = Logger()

    logger.info(
        Log(
            title="Going to search user_query",
            file=__name__,
            funcname="search",
            request=user_query,
        )
    )
    statement: UserQueryStatement = UserQueryStatement(query=user_query)
    result: list[Document]  = SearchDocService().find(statement.query)
    logger.debug(
        Log(
            title="Response from search user_query",
            file=__name__,
            funcname="search",
            request=user_query,
            response=result,
        )
    )

    documents = [
        {"code": document.code, "similarity": document.similarity}
        for document in result
    ]
    logger.info(
        Log(
            title="Found documents",
            file=__name__,
            funcname="search",
            request=user_query,
            response=documents,
        )
    )
    return SearchDocsResponse(documents=documents)


