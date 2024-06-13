### Document schema ###

def document_schema(document) -> dict:
    return {"code": document["code"],
            "similarity": document["similarity"],
            }

def document_list_schema(doc_list) -> list:
    return [document_schema(doc) for doc in doc_list]