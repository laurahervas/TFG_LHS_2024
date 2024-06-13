from fastapi import FastAPI
from routers import users_db
from services.refresh_emb_service import RefreshEmbeddings
from routers import jwt_auth_users, embeddings_db, corpus_db, prompt_db, conversation_db
from dotenv import load_dotenv
from pathlib import Path

import uvicorn
import os

app = FastAPI()

app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.include_router(embeddings_db.router)
app.include_router(corpus_db.router)
app.include_router(prompt_db.router)
app.include_router(conversation_db.router)

environment = os.getenv("APP_ENV", "dev")
path = f".env.{environment}"
print(f"Loading environment variables from: {path}")    
load_dotenv(dotenv_path=Path(path))

# Url local: http://127.0.0.1:8000

refresh_embeddings = RefreshEmbeddings()
refresh_embeddings.execute()

@app.get("/")
async def root():
    return "Backend UOCBank"

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",  port=int(os.getenv("APP_PORT")),reload=True)