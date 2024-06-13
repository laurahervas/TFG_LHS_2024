import json
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status
from db.schemas.conversation import conversation_schema, conversations_schema
from db.models.conversation import Conversation
from db.client import db_client
from bson import ObjectId
import os
import pandas as pd
from services.logger import Logger
from domain.models.log import Log


router = APIRouter(prefix="/conversation",
                   tags=["conversation"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Conversacion no encontrada"}})

@router.get("/all", response_model=list[Conversation])
async def all_conversation():
    logger = Logger()
    logger.debug(
        Log(
            title="get all conversations from DB",
            file=__name__,
            funcname="all_conversation",
        )
    )
    all_conversations = db_client.conversations.find()
    logger.info(
        Log(
            title="get all conversations from DB",
            file=__name__,
            funcname="all_conversation",
            response=all_conversations,
        )
    )
    return conversations_schema(all_conversations)

@router.get("/user/{user}")  # Path
async def conversations_user(user: str):
    logger = Logger()
    logger.debug(
        Log(
            title="search conversation for user ",
            file=__name__,
            funcname="conversations_user",
            request=user,
        )
    )
    user_conversations = search_user_conversations(user,logger)
    logger.info(
        Log(
            title="search conversation for user ",
            file=__name__,
            funcname="conversations_user",
            request=user,
            response=user_conversations,
        )
    )
    return user_conversations

@router.get("/{id}")  # Path
async def conversation(id: str):
    logger = Logger()
    logger.info(
        Log(
            title="search conversation with id",
            file=__name__,
            funcname="conversation",
            request=id,
        )
    )
    return search_conversation("_id",ObjectId(id),logger)

@router.get("/")  # Query
async def conversation(id: str):
    logger = Logger()
    logger.info(
        Log(
            title="search conversation with id",
            file=__name__,
            funcname="conversation",
            request=id,
        )
    )
    return search_conversation("_id",ObjectId(id), logger)

@router.post("/", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def conversation(conv: Conversation):
    logger = Logger()
    conv_dict = dict(conv)
    logger.debug(
        Log(
            title="Going to add conversation to DB",
            file=__name__,
            funcname="conversation",
            request=conv_dict,
        )
    )
    
    if conv.id !=None and type(search_conversation("_id",ObjectId(conv.id), logger)) == Conversation:
        logger.error(
            Log(
                title="Error conversation already exists",
                file=__name__,
                funcname="conversation",
                request=conv_dict,
            )
        )
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail="La conversación ya existe")
    
    id = db_client.conversations.insert_one(conv_dict).inserted_id
    new_conv = conversation_schema(db_client.conversations.find_one({"_id": id}))
    logger.info(
        Log(
            title="Response from adding conversation to DB",
            file=__name__,
            funcname="conversation",
            request=new_conv,
        )
    )
    return Conversation(**new_conv)

@router.put("/", response_model=Conversation,status_code=status.HTTP_202_ACCEPTED)
async def conversation(conv: Conversation):
    logger = Logger()
    #actualizar las conversaciones
    try:
        conv_dict = dict(conv)
        logger.debug(
            Log(
                title="Update conversation to DB",
                file=__name__,
                funcname="conversation",
                request=conv_dict,
            )
        )

        old_conversation = search_conversation("_id",ObjectId(conv_dict["id"]), logger)
        convers_to_update = old_conversation.conversation
        logger.debug(
            Log(
                title="Old conversation to update",
                file=__name__,
                funcname="conversation",
                request=convers_to_update,
            )
        )
        for each_conv in convers_to_update:

            if each_conv["query"] == conv_dict["conversation"][0]["query"]:
                logger.debug(
                    Log(
                        title="Remove conversation prior to update",
                        file=__name__,
                        funcname="conversation",
                        request=each_conv,
                    )
                )
                convers_to_update.remove(each_conv)
                break
        
        #update conversation
        conv_list = conv_dict["conversation"]
        for eachconv in conv_list:
            convers_to_update.append({"query":eachconv["query"],"response":eachconv["response"]})

        conv.conversation = convers_to_update
        new_conv_dict = dict(conv)
        logger.debug(
            Log(
                title="Going to update conversation",
                file=__name__,
                funcname="conversation",
                request=new_conv_dict,
            )
        )
        convers_user = db_client.conversations.find_one_and_replace({"_id": ObjectId(conv_dict["id"])}, new_conv_dict)
        
        #[{"query":conv_dict["conversation"]["query"],"response":conv_dict["conversation"]["response"]},]
        if(convers_user == None):
            logger.error(
                Log(
                    title="Exception updating conversation in DB",
                    file=__name__,
                    funcname="conversation",
                    request=new_conv_dict,
                )
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La conversacion no se ha actulizado")
        
        logger.info(
            Log(
                title="Updated conversation in DB",
                file=__name__,
                funcname="conversation",
                request=new_conv_dict,
                response=convers_user,
            )
        )
    except Exception as e:
        error = f"Exception during updating the conversation: {e}"
        logger.error(
            Log(
                title="Exception updating conversation in DB",
                file=__name__,
                funcname="conversation",
                request=new_conv_dict,
                response=error,
            )
        )
        return {"error": error}

    return search_conversation("_id", ObjectId(conv_dict["id"]), logger)

def search_conversation(field: str, key, logger: Logger):
    try:
        find_conversation = f"search conversation with {field}: {key}"
        logger.debug(
            Log(
                title="Going to search conversation with field and key",
                file=__name__,
                funcname="search_conversation",
                request=find_conversation,
            )
        )
        conv = db_client.conversations.find_one({field: key})
        logger.info(
            Log(
                title="Response from search conversation with field and key",
                file=__name__,
                funcname="search_conversation",
                request=find_conversation,
                response=conv,
            )
        )
        return Conversation(**conversation_schema(conv))

    except Exception as e:
        error = f"Exception: could not be found search conversation by field {field} code: {key} error: {e}"
        logger.error(
            Log(
                title="Exception from search conversation with field and key",
                file=__name__,
                funcname="search_conversation",
                request=find_conversation,
                response=error,
            )
        )
        return {"error": "No se ha encontrado la conversación"}

def search_user_conversations(key, logger: Logger):
    try:
        find_conversation = f"search user {key} conversation"
        logger.debug(
            Log(
                title="Going to search user conversation",
                file=__name__,
                funcname="search_user_conversations",
                request=find_conversation,
            )
        )
        convList = db_client.conversations.find({"user": int(key)})
        logger.debug(
            Log(
                title="Responsse from search user conversation",
                file=__name__,
                funcname="search_user_conversations",
                request=find_conversation,
                response=convList,
            )
        )
        return conversations_schema(convList)

    except Exception as e:
        error = f"Exception: could not be found user{key} conversation error: {e}"
        logger.error(
            Log(
                title="Exception search user conversation",
                file=__name__,
                funcname="search_user_conversations",
                request=find_conversation,
                response=error,
            )
        )
        return {"error": "No se ha encontrado ninguna conversacion para el usuario: "+ key}
    

@router.delete("/clean", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversations():
    logger = Logger()
    try:
        #delete all the conversations in database
        logger.debug(
            Log(
                title="Going to delete all conversation in DB",
                file=__name__,
                funcname="delete_conversations",
            )
        )
        db_client.conversations.delete_many({})
        logger.info(
            Log(
                title="Delete all conversations in DB",
                file=__name__,
                funcname="delete_conversations",
            )
        )
        return {"message": "Conversaciones eliminadas"}
    except Exception as e:
        message = f"Exception: cleaning the conversations {e}"
        logger.error(
            Log(
                title="Delete all conversations in DB",
                file=__name__,
                funcname="delete_conversations",
                response=message,
            )
        )
        return {"error": message}