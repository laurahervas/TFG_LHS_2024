### Corpus schema ###

def corpus_schema(corpus) -> dict:
    return {"id": str(corpus["_id"]),
            "code": corpus["code"],
            "title": corpus["title"],
            "texto": corpus["texto"],
            "variaciones": corpus["variaciones"],
            "num_variaciones": int(corpus["num_variaciones"]),
            "motivo": corpus["motivo"],
            "intent": corpus["intent"],
            "num_tokens": int(corpus["num_tokens"]),
            }

def corpus_list_schema(corpus_list) -> list:
    return [corpus_schema(corpus) for corpus in corpus_list]