### Conversation schema ###

def conversation_schema(conversation) -> dict:
    return {"id": str(conversation["_id"]),
            "user": conversation["user"],
            "conversation": conversation["conversation"],}


def conversations_schema(conversations) -> list:
    return [conversation_schema(conversation) for conversation in conversations]