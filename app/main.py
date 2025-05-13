from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import user, todo

app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "FastAPI is working!"}
