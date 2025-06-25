import pre_patch 
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
from app.routes import horarios, usuarios

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(horarios.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Bienvenidos a mi api de horarios, made by t.me/benjaaa1 & team."}