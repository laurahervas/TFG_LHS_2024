import json
from fastapi import APIRouter
from fastapi import APIRouter, HTTPException, status
from db.schemas.prompt import prompt_schema, prompts_schema
from db.models.prompt import Prompt
from db.client import db_client
from bson import ObjectId
import os
import pandas as pd
from services.logger import Logger
from domain.models.log import Log

router = APIRouter(prefix="/prompt",
                   tags=["prompt"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "Prompt No encontrado"}})

@router.get("/", response_model=list[Prompt])
async def prompt():
    return prompts_schema(db_client.prompts.find())

@router.get("/code/{code}")  # Path
async def prompts(code: str):
    logger = Logger()

    logger.info(
        Log(
            title="Search prompt with code ",
            file=__name__,
            funcname="getPrompt",
            request=code,
        )
    )
    return search_code_prompt(code, logger)

@router.get("/")  # Query
async def prompt(id: str):
    logger = Logger()

    logger.info(
        Log(
            title="Search prompt with id ",
            file=__name__,
            funcname="getPrompt",
            request=id,
        )
    )
    return search_prompt("_id",ObjectId(id),logger)


@router.get("/reload_prompts", response_model=list[Prompt])
async def reload_prompts():
    logger = Logger()

    promptList = []
    
    #clean all the prompts in database
    db_client.prompts.delete_many({})
    promptsPath = os.getenv("PROMPT_JSON")
    logger.info(
        Log(
            title="Reload prompts from",
            file=__name__,
            funcname="reload_prompts",
            request=promptsPath,
        )
    )

    with open(promptsPath, "r") as file:
        data = json.load(file)
        logger.debug(
            Log(
                title="loaded prompts from file",
                file=__name__,
                funcname="reload_prompts",
                request=data,
            )
        )

    # Create Prompt objects from the data
    for row in data:
        code = row['code']
        name = row['name']
        prompt = row['prompt']

        newPrompt = Prompt(code=code, name=name, prompt=prompt)
        promptList.append(newPrompt)
        addPromptToDB(newPrompt, logger)
    logger.debug(
        Log(
            title="Added prompts to list",
            file=__name__,
            funcname="reload_prompts",
            request=promptList,
        )
    )
    return promptList

def addPromptToDB(prompt: Prompt, logger: Logger):
    prompt_dict = dict(prompt)
    del prompt_dict["id"]

    id = db_client.prompts.insert_one(prompt_dict).inserted_id
    
    new_entry = prompt_schema(db_client.prompts.find_one({"_id": id}))
    logger.debug(
        Log(
            title="Adding prompt to DB",
            file=__name__,
            funcname="addPromptToDB",
            request=new_entry,
        )
    )
    return Prompt(**new_entry)

  
def search_prompt(field:str, key, logger: Logger):
    try:
        find_prompt = f"{field}: {key}"
        logger.debug(
            Log(
                title="Going to search for prompt",
                file=__name__,
                funcname="search_prompt",
                request=find_prompt,
            )
        )
        prompt= db_client.prompt.find_one({field: key})
        logger.info(
            Log(
                title="Response getting prompt",
                file=__name__,
                funcname="search_prompt",
                request=find_prompt,
                response=prompt,
            )
        )
        return Prompt(**prompt_schema(prompt))

    except Exception as e:
        error = {"error": "No se ha encontrado el prompt"}
        message = f"Exception searching prompt field: {field} code: {key} error {e}"

        logger.error(
            Log(
                title="Exception getting prompt",
                file=__name__,
                funcname="search_prompt",
                request=message,
            )
        )
        return error

def search_code_prompt(key, logger: Logger):
    try:
        find_prompt = f"code: {key}"
        logger.debug(
            Log(
                title="Going to search for prompt with code",
                file=__name__,
                funcname="search_prompt",
                request=find_prompt,
            )
        )
        prompt= db_client.prompts.find_one({"code": int(key)})
        logger.info(
            Log(
                title="Response getting prompt wih code",
                file=__name__,
                funcname="search_prompt",
                request=find_prompt,
                response=prompt,
            )
        )
        return Prompt(**prompt_schema(prompt))

    except Exception as e:
        error = {"error": "No se ha encontrado el prompt"}
        message = f"Exception searching prompt code: {key} error {e}"
        logger.error(
            Log(
                title="Exception getting prompt",
                file=__name__,
                funcname="search_prompt",
                request=message,
            )
        )
        return error