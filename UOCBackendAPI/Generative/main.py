from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path
from routers import generative_router

import uvicorn
import os

app = FastAPI()

# Url local: http://127.0.0.1:8000
app.include_router(generative_router.router)

environment = os.getenv("APP_ENV", "dev")
path = f".env.{environment}"
print(f"Loading environment variables from: {path}")    
load_dotenv(dotenv_path=Path(path))

@app.get("/")
async def root():
    return "Hola FastAPI!"

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
print("APP_PORT", os.getenv("APP_PORT"))
if __name__ == '__main__':
    #uvicorn.run(app, host="0.0.0.0",  port=8001)
    uvicorn.run(app, host="0.0.0.0",  port=int(os.getenv("APP_PORT")),reload=True)