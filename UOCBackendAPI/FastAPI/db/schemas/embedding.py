### Embedding schema ###

def embedding_schema(embedding) -> dict:
    return {"id": str(embedding["_id"]),
            "code": embedding["code"],
            "embeddings": embedding["embeddings"],
            "motivo": embedding["motivo"],}



def embeddings_schema(embeddings) -> list:
    return [embedding_schema(embedding) for embedding in embeddings]