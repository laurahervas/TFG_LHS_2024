
from fastapi import APIRouter, status

from services.generative_service import GenerativeService
from services.prompt_service import PromptService
from services.corpus_service import CorpusService
from services.conversation_service import ConversationService
from domain.models.document import Document
from services.search_service import SearchService
from models.generate_request import GenerateRequest
from models.generate_response import GenerateResponse
from domain.models.prompt_type import PromptType
from domain.models.log import Log
from services.logger import Logger
import pandas as pd
import json
import re
import os

router = APIRouter(prefix="/generative",
                   tags=["generative"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.post("/generate", response_model=GenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate(request: GenerateRequest) -> GenerateResponse:
    logger = Logger()

    bCard: bool = False
    logger.info(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Start generate request",
            file=__name__,
            funcname="generate",
            request=request.model_dump_json(),
            user_id=request.user
        )
    )
    #detect subject of the conversation
    bCard = checkSubject(request, logger)
    if bCard == False:
        logger.info(        
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Subject is not card -> call generative service APOLOGIZE",
                file=__name__,
                funcname="generate",
                request=request.model_dump_json(),
                user_id=request.user
            )
        )
        result = callGenerativeService(PromptType.APOLOGIZE, request, logger)
        Logger().info(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Answer [APOLOGIZE]",
                file=__name__,
                funcname="generate",
                request=request.model_dump_json(),
                response=result.choices[0].message.content,
                user_id=request.user
            )
        )
        return GenerateResponse(answer=result.choices[0].message.content, tokens=result.usage.total_tokens)
    
    logger.debug(  
        Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Looking for conversation -> call DB",
                file=__name__,
                funcname="generate",
                request=request.model_dump_json(),
                user_id=request.user
            )
    )
    convsrv = ConversationService()
    if request.conversation != None and  request.conversation != "":
        conv = convsrv.findConversation(request.conversation)
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Conversation found",
                file=__name__,
                funcname="generate",
                response=conv.parsedResponse,
                user_id=request.user
            )
        )

    else:
        conv = convsrv.createConversation(request.user, request.query)
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Conversation created",
                file=__name__,
                funcname="generate",
                response=conv.parsedResponse,
                user_id=request.user
            )
        )
    searchResponse = SearchService().search(request.query)
    search_response = searchResponse.documents
    codePrompt = ""
    corpusList = None    

    if len(search_response) > 0:
        search_response = sorted(search_response, key=lambda x: x.similarity, reverse=True)
        
        corpusList = findCorpusByList(search_response)
        corpusDocs = [corpus["code"] for corpus in corpusList]
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Extracting documents from corpus",
                file=__name__,
                funcname="generate",
                request=search_response,
                response=corpusDocs,
                user_id=request.user
            )
        )
        codePrompt = PromptType.getcode(PromptType.GENERATE_SIMPLE)
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Getting prompt for GENERATE_SIMPLE",
                file=__name__,
                funcname="generate",
                response=codePrompt,
                user_id=request.user
            )
        )
    else:
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="No corpus found. Going to ask for REFORMULATE",
                file=__name__,
                funcname="generate",
                user_id=request.user
            )
        )
        codePrompt = PromptType.getcode(PromptType.REFORMULATE)
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="No corpus found. Getting prompt code for REFORMULATE",
                file=__name__,
                funcname="generate",
                response=codePrompt,
                user_id=request.user
            )
        )

    prompt_data = PromptService().getPrompt(codePrompt)
    prompt_prompt = str(prompt_data.prompt.prompt)
    prompt_prompt = prompt_prompt.replace("{user_query}", request.query)
    prompt_data = prompt_prompt
    logger.debug(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Prompt data to call generative",
            file=__name__,
            funcname="generate",
            response=prompt_data,
            user_id=request.user
        )
    )
    if corpusList is not None:
        input_documents = ""
        for corpus in corpusList:
            input_documents += "\nDocumento " + str(corpus["code"]) + ": " + corpus["title"] + " --- " + corpus["texto"]
        
        prompt_data = prompt_prompt.replace("{documents}", input_documents)
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Adding documents to insert in Prompt before calling generative",
                file=__name__,
                funcname="generate",
                response=input_documents,
                user_id=request.user
            )
        )
    else:
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Any documents found to add in Prompt before calling generative",
                file=__name__,
                funcname="generate",
                user_id=request.user
            )
        )

    prompt = [{ "role": "system", "content": prompt_data }]  
    logger.debug(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Going to call generative",
            file=__name__,
            funcname="generate",
            request=prompt,
            user_id=request.user
        )
    )
    result = GenerativeService().generative(prompt, request.query)
      
    if len(result.choices) == 0:
        logger.error(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Error in response",
                file=__name__,
                funcname="generate",
                request=prompt,
                response=result.choices[0].message.content,
                user_id=request.user
            )
        )
        return GenerateResponse(answer="Error in response", tokens=3)
    logger.info(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Response from generative",
            file=__name__,
            funcname="generate",
            request=prompt,
            response=result.choices[0].message.content,
            user_id=request.user
        )
    )
    report = evaluateModel(request.user, request.query, corpusList, result.choices[0].message.content, logger)
    logger.info(
        Log(
            user_id=request.user,
            convesation_id=request.conversation,
            user_query=request.query,            
            title="Response from generative EVALUATION_MODEL",
            file=__name__,
            funcname="generate",
            request=result.choices[0].message.content,
            response=report
        )
    )

    convFromDB = conv.parsedResponse
    logger.debug(
        Log(
            user_id=request.user,
            convesation_id=request.conversation,
            user_query=request.query,            
            title="Going to update conversation in DB with response",
            file=__name__,
            funcname="generate",
            request=request.query,
            response=result.choices[0].message.content
        )
    )

    conv = convsrv.updateConversation(convFromDB["id"], request.user, request.query,result.choices[0].message.content)
    if(conv == None):
        logger.error(
            Log(
                user_id=request.user,
                convesation_id=request.conversation,
                user_query=request.query,            
                title="Error in updating conversation",
                file=__name__,
                funcname="generate",
                request=request.query,
                response=convFromDB
            )
    )
    return GenerateResponse(answer=result.choices[0].message.content, tokens=result.usage.total_tokens)
    
def findCorpusByCode(corpus_doc_code: str):

    searchResponse = CorpusService().findDoc(corpus_doc_code)
    return searchResponse

def findCorpusByList(corpus_docs: list[Document]):
    searchResponse = CorpusService().findListDocs(corpus_docs)
    return searchResponse.corpusList

def extract_topic(text: str, logger: Logger):
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        logger.debug(
            Log(
                convesation_id="",
                user_query=text,
                title="Going to find json",
                file=__name__,
                funcname="extract_topic",
                response=match
            )
        )
        if match:
            json_text =  match.group(0)
            json_text = re.sub(r'\'', '"', json_text)
            json_topic = json.loads(json_text)
            topic =json_topic['topic']
            if "TARJETA" == topic.upper() or "CARD" == topic.upper() or 'TARJETA' == topic.upper() or 'CARD' == topic.upper():
                logger.debug(
                    Log(
                        convesation_id="",
                        user_query=text,
                        title="Formatted json:",
                        file=__name__,
                        funcname="extract_topic",
                        response=topic
                    )
                )   
                return True
            else:
                logger.debug(
                    Log(
                        convesation_id="",
                        user_query=text,
                        title="Card not detected:",
                        file=__name__,
                        funcname="extract_topic",
                        response=topic
                    )
                )   
                pass
    except Exception as e:
        logger.error(
            Log(
                convesation_id="",
                user_query=text,
                title="EXCEPTION in extract_topic:",
                file=__name__,
                funcname="extract_topic",
                response=e
            )
        )   
        pass
    return None

def checkSubject(request: GenerateRequest, logger: Logger) -> bool:
    bCard = False
    logger.debug(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Entering function checking CARD topic",
            file=__name__,
            funcname="checkSubject",
            user_id=request.user
        )
    )
    codePrompt = PromptType.getcode(PromptType.CHECK_SUBJECT)
    prompt_data = PromptService().getPrompt(codePrompt)
    prompt_tmp = prompt_data.prompt.prompt
    prompt_prompt = prompt_tmp.replace("{user_query}", request.query)
    prompt = [{ "role": "system", "content": prompt_prompt }]
    logger.debug(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Going to call generative CHECK_SUBJECT",
            file=__name__,
            funcname="checkSubject",
            request=prompt,    
            user_id=request.user
        )
    )
    result = GenerativeService().generative(prompt, request.query)
    if result == None or result == "":
        
        logger.debug(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Error detecting topic",
                file=__name__,
                funcname="checkSubject",
                user_id=request.user
            )
        )
    else:
        resultText = result.choices[0].message.content
        
        logger.info(
            Log(
                convesation_id=request.conversation,
                user_query=request.query,
                title="Response topic detected",
                file=__name__,
                funcname="checkSubject",
                request=prompt,
                response=resultText,
                user_id=request.user
            )
        )
        
        resultText.removeprefix("===")
        if(extract_topic(resultText, logger)):
            bCard = True
            logger.debug(
                Log(
                    convesation_id=request.conversation,
                    user_query=request.query,
                    title="Response CARD detected",
                    file=__name__,
                    funcname="checkSubject",
                    user_id=request.user
                )
            )
    return bCard

def callGenerativeService(promptType: PromptType, request: GenerateRequest, logger: Logger):
    logger.debug(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Going to call Generative",
            file=__name__,
            funcname="callGenerativeService",
            request=promptType.toString(),
            user_id=request.user
        )
    )
    codePrompt = PromptType.getcode(promptType)
    prompt_data = PromptService().getPrompt(codePrompt)
    prompt_prompt = prompt_data.prompt.prompt
    if(request.query == None or request.query == ""):
        prompt_prompt = prompt_data.prompt.prompt.replace("{user_query}", request.query)
    prompt = [{ "role": "system", "content": prompt_prompt }]  
    result = GenerativeService().generative(prompt, request.query)
    logger.debug(
        Log(
            convesation_id=request.conversation,
            user_query=request.query,
            title="Response from Generative",
            file=__name__,
            funcname="callGenerativeService",
            request=promptType.toString(),
            response=result.choices[0].message.content,
            user_id=request.user
        )
    )
    return result

def extract_fuentes(text: str, logger: Logger):
    logger.debug(
        Log(
            title="Extracting sources from response",
            file=__name__,
            funcname="extract_fuentes",
            request=text,
        )
    )
    matches = re.findall(r'\{.*?\}', text, re.DOTALL)
    if len(matches) >= 0:
        for match in matches:
            try:
                json_text = re.sub(r'\'', '"', match)
                keyMatch, bfound = getMatchedWord (json_text)
                if bfound:
                    json_text = json.loads(json_text)
                    if json_text[keyMatch] is not None:
                        source = json_text[keyMatch]
                        logger.debug(
                            Log(
                                title=f"key {keyMatch} detected",
                                file=__name__,
                                funcname="extract_fuentes",
                                request=match,
                                response=source
                            )
                        )
                        return source
            except Exception as e:
                logger.error(
                    Log(
                        title="Exception detecting key \"sources\"",
                        file=__name__,
                        funcname="extract_fuentes",
                        request=match,
                        response=e
                    )
                )
                pass
    return None

def getMatchedWord (text: str):
    if "fuentes" in text.lower():
        return "fuentes", True
    elif "sources" in text.lower():
        return "sources", True
    else:
        return "", False
    
def evaluateModel(user: str, query: str, corpusList: list, response: str, logger: Logger):
    logger.debug(
        Log(
            user_id=user,
            user_query=query,            
            title="Evaluation model adding EVALUATION_MODEL_USER",
            file=__name__,
            funcname="evaluateModel",
            request=corpusList,
            response=response
        )
    )
    eval_prompt_user = PromptType.getcode(PromptType.EVALUATION_MODEL_USER)
    prompt_data = PromptService().getPrompt(eval_prompt_user)
    prompt_data_user = prompt_data.prompt.prompt
    content_user = prompt_data_user.replace("{query}", query)
    content_user = content_user.replace("{generated_answer}", response)
    texto = ""
    if corpusList is not None:
        sourceList = extract_fuentes(response,logger)
        if sourceList is not None and len(corpusList) > 0:
            for source in sourceList:
                for corpus in corpusList:
                    if corpus["code"] == int(source):
                        texto += corpus["texto"] + " "
                        logger.debug(
                            Log(
                                user_id=user,
                                user_query=query,            
                                title="Adding reference answer",
                                file=__name__,
                                funcname="evaluateModel",
                                request=texto,
                            )
                        )
                        break
    
    if texto == "":
        response = "No se ha encontrado documentos en la respuesta generada. No se puede obtener groundtruth para evaluar la respuesta."
        logger.error(
            Log(
                user_id=user,
                user_query=query,            
                title="Extracting sources from response",
                file=__name__,
                funcname="evaluateModel",
                request=corpusList,
                response=response
            )
        )
        return {"passing": False, "score": 0, "reason": "Error evaluating the response"}
    
    content_user = content_user.replace("{reference_answer}",  texto)
    logger.debug(
        Log(
            user_id=user,
            user_query=query,            
            title="Evaluation model adding EVALUATION_MODEL_SYSTEM",
            file=__name__,
            funcname="evaluateModel",
            request=content_user,
        )
    )
    eval_prompt_system = PromptType.getcode(PromptType.EVALUATION_MODEL_SYSTEM)
    prompt_data_sys = PromptService().getPrompt(eval_prompt_system)
    content_system = prompt_data_sys.prompt.prompt

    messages = [{ "role": "system", "content": content_system },{ "role": "user", "content": content_user } ]
    logger.debug(
        Log(
            user_id=user,
            user_query=query,            
            title="Going to call generative EVALUATION_MODEL",
            file=__name__,
            funcname="evaluateModel",
            request=messages,
        )
    )

    result = GenerativeService().generative(messages, query)

    if(result == None):
        logger.debug(
            Log(
                user_id=user,
                user_query=query,            
                title="Response from generative in EVALUATION_MODEL",
                file=__name__,
                funcname="evaluateModel",
                request=messages,
                response=result
            )
        )
        return {"passing": False, "score": 0, "reason": "Error in response"}
    raw_output = result.choices[0].message.content

    # Extract from response
    score_str, reasoning_str = raw_output.split("\n", 1)
    score = float(score_str)
    reasoning = reasoning_str.lstrip("\n")
    threshold = float(os.getenv("EVALUATION_THRESHOLD"))
    logger.debug(
        Log(
            user_id=user,
            user_query=query,            
            title="Response from generative in EVALUATION_MODEL",
            file=__name__,
            funcname="evaluateModel",
            request=messages,
            response=raw_output
        )
    )

    return {"passing": score >= threshold, "score": score, "reason": reasoning}


