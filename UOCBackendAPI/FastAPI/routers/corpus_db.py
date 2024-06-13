
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status
from db.models.corpus_response import CorpusDocsResponse
from db.models.document import Document
from db.schemas.corpus import corpus_schema, corpus_list_schema
from db.models.corpus import Corpus
from domain.models.corpus import Corpus as CorpusModel
from db.client import db_client
from bson import ObjectId
import os
import json
import pandas as pd
from services.logger import Logger
from domain.models.log import Log


router = APIRouter(prefix="/corpus",
                   tags=["corpus"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})



@router.get("/", response_model=list[Corpus])
async def corpus():
    return corpus_list_schema(db_client.corpus.find())

@router.get("/code/{code}",response_model=Corpus)  # Path
async def corpus(code: str):
    logger = Logger()

    logger.debug(
        Log(
            title="Going to search corpus with code ",
            file=__name__,
            funcname="corpus",
            request=code,
        )
    )
    corpus = search_code_corpus(code,logger)
    logger.debug(
        Log(
            title="Response from search corpus with code ",
            file=__name__,
            funcname="corpus",
            request=code,
            response=corpus,
        )
    )
    return corpus


@router.get("/")  # Query
async def corpus(id: str):
    return search_corpus("_id",ObjectId(id))


@router.get("/reload_corpus", response_model=list[Corpus])
async def reload_corpus():
    logger = Logger()
    corpusList = []
    
    #delete all the embeddings in database
    db_client.corpus.delete_many({})
    corpus = os.getenv("CORPUS_PKL")
    logger.debug(
        Log(
            title="Reload corpus from",
            file=__name__,
            funcname="reload_corpus",
            request=corpus,
        )
    )
    corpusPickle = pd.read_pickle(corpus)

    lines = corpusPickle
    
    logger.debug(
        Log(
            title="loaded corpus from file",
            file=__name__,
            funcname="reload_prompts",
            request=lines,

        )
    )

    for index, row in lines.iterrows():
        code = row['CODIGO_FAQ']
        title = row['title_found']
        texto = row['body texto']
        variaciones = row['variaciones']
        num_variaciones = int(row['num_variaciones'])
        motivo = row['motivo']
        if pd.isnull(motivo):
            motivo = ""
        else:
            motivo = str(int(motivo))
        intent = row['intent']
        num_tokens = int(row['num_tokens'])
        
        newCorpus = Corpus(code=code, title=title, texto=texto, variaciones=variaciones,num_variaciones=num_variaciones, motivo=motivo,intent=intent,num_tokens=num_tokens)
        corpusList.append(newCorpus)
        addCorpusToDB(newCorpus,logger)
    
    logger.debug(
        Log(
            title="Added corpus from file to DB",
            file=__name__,
            funcname="reload_prompts",
            response=corpusList,

        )
    )
    return corpusList

@router.get("/codelist", response_model=CorpusDocsResponse)
async def search_codes_corpus(docList: list[Document]):
    logger = Logger()
    logger.debug(
        Log(
            title="Going to search corpus by codelist",
            file=__name__,
            funcname="search_codes_corpus",
            request=docList,
        )
    )
    codes = [obj.code for obj in docList]

    corpusDocs: list[CorpusModel]  = search_corpus_by_list(codes, logger)
    
    if corpusDocs == []:
        return CorpusDocsResponse(corpus=[])

    corpus_list = [
        {"code": doc.code, "title": doc.title, "texto": doc.texto, "variaciones": doc.variaciones, "num_variaciones": doc.num_variaciones, "motivo": doc.motivo, "intent": doc.intent, "num_tokens": doc.num_tokens}
        for doc in corpusDocs
    ]
    return CorpusDocsResponse(corpus=corpus_list)
    

def addCorpusToDB(corpus: Corpus, logger: Logger):
    corpus_dict = dict(corpus)
    del corpus_dict["id"]
    logger.debug(
        Log(
            title="Going to add corpus to DB",
            file=__name__,
            funcname="addCorpusToDB",
            request=corpus_dict,
        )
    )
    id = db_client.corpus.insert_one(corpus_dict).inserted_id
    logger.debug(
        Log(
            title="Response from adding corpus to DB",
            file=__name__,
            funcname="addCorpusToDB",
            request=corpus_dict,
            response=id,
        )
    )

    #comprobar si el id está en la base de datos
    #el nombre de la clave unica del id es _id
    new_entry = corpus_schema(db_client.corpus.find_one({"_id": id}))
    
    return Corpus(**new_entry)

  
def search_corpus(field:str, key, logger: Logger):
    try:
        find_corpus = f"search corpus with {field}: {key}"
        logger.debug(
            Log(
                title="Going to search corpus with field and key ",
                file=__name__,
                funcname="search_corpus",
                request=find_corpus,
            )
        )
        corpus= db_client.corpus.find_one({field: key})
        logger.debug(
            Log(
                title="Response from search corpus with field and key ",
                file=__name__,
                funcname="search_corpus",
                request=find_corpus,
                response=corpus,
            )
        )
        return Corpus(**corpus_schema(corpus))

    except Exception as e:
        error = f"Exception during searching document in corpus: {e}"
        logger.error(
            Log(
                title="Response from search corpus with field and key ",
                file=__name__,
                funcname="search_corpus",
                request=find_corpus,
                response=error,
            )
        )
        #raise HTTPException(status_code=400, detail="code not found in corpus")
        return None

def search_code_corpus(key,logger: Logger):
    code=F"code: {key}"
    try:
        logger.debug(
            Log(
                title="Going to search corpus with code",
                file=__name__,
                funcname="search_code_corpus",
                request=code,
            )
        )
        corpus= db_client.corpus.find_one({"code": int(key)})
        logger.debug(
            Log(
                title="Response from search corpus with code",
                file=__name__,
                funcname="search_code_corpus",
                request=key,
                response=corpus,
            )
        )
        return Corpus(**corpus_schema(corpus))
    except Exception as e:
        error = f"Exception: During search corpus by code: {key} error: {e}"
        logger.error(
            Log(
                title="Response from search corpus with code ",
                file=__name__,
                funcname="search_code_corpus",
                request=key,
                response=error,
            )
        )
        #raise HTTPException(status_code=400, detail=message)
        return None

def search_corpus_by_list(codes: list, logger: Logger):
    corpusList = []
    logger.debug(
        Log(
            title="Going to search corpus by codelist",
            file=__name__,
            funcname="search_corpus_by_list",
            request=codes,
        )
    )
    try:
        for code in codes:
            corpus = search_code_corpus(code, logger)
            if corpus is None:
                logger.debug(
                    Log(
                        title="Search corpus by code could not be found in DB",
                        file=__name__,
                        funcname="search_corpus_by_list",
                        request=code,
                    )
                )
            else:
                corpusList.append(corpus)
        logger.debug(
            Log(
                title="Response from search corpus by codelist",
                file=__name__,
                funcname="search_corpus_by_list",
                request=codes,
                response=corpusList,
            )
        )    
    except Exception as e:
        message = f"Exception: searching corpus by code list in DB {e}"
        
        logger.error(
            Log(
                title="Search corpus by code list in DB",
                file=__name__,
                funcname="search_corpus_by_list",
                response=message,
            )
        )

    return corpusList