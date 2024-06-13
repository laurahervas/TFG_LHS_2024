### Prompt schema ###

def prompt_schema(prompt) -> dict:
    return {"id": str(prompt["_id"]),
            "code": prompt["code"],
            "name": prompt["name"],
            "prompt": prompt["prompt"],}



def prompts_schema(prompts) -> list:
    return [prompt_schema(prompt) for prompt in prompts]