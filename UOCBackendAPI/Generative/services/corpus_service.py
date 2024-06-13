from fastapi import Depends
import json
import os

from domain.models.corpus_response import CorpusResponse
from domain.models.corpus import Corpus
from domain.models.document import Document
from services.handle_request import HandleRequest
from services.logger import Logger
from domain.models.log import Log

class CorpusService:
    def __init__(
        self,
    ):
        self.handle_request = HandleRequest()
        self.baseUrl = os.getenv("MS_CORPUS_URL")
        self.logger = Logger()


    def findListDocs(self, docs: list[Document]) -> list[Corpus]:
        url = f"{self.baseUrl}/codelist"
        listDocs=[]
        for doc in docs:
            data_dict = {'code':str(doc.code), 'similarity':round(doc.similarity,3)}
            listDocs.append(data_dict)
        self.logger.debug(
            Log(
                title="Going to call FastAPI for corpus docs",
                file=__name__,
                funcname="findListDocs",
                request=listDocs,
            )
        )
        
        response = self.handle_request.getdata(
            url=url,
            params={"listdocs": listDocs},
            data=listDocs
        )
        self.logger.debug(
            Log(
                title="Response from FastAPI for corpus listdocs",
                file=__name__,
                funcname="findListDocs",
                request=listDocs,
                response=response.text,
            )
        )
        return CorpusResponse(response.text)
       
    def findDoc(self, code:str) -> list[Corpus]:
        url = f"{self.baseUrl}/code/{code}"
        self.logger.debug(
            Log(
                title="Response from FastAPI for corpus doc",
                file=__name__,
                funcname="findDoc",
                request=code,
            )
        )
        response = self.handle_request.get(
            url=url,
            params={}
        )
        self.logger.debug(
            Log(
                title="Response from FastAPI for corpus doc",
                file=__name__,
                funcname="findDoc",
                request=code,
                response=response.text,
            )
        )
        return CorpusResponse(response.text)
    

