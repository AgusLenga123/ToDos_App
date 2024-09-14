# Logic File

from fastapi import FastAPI, Depends, HTTPException, Path
import models as models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

# Creation of the database from the model passed (only run if todos.db does not exist, because it creates the database)
models.Base.metadata.create_all(bind=engine)

# Fun to open db for API requests:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# depends = dependency injection. Function relies on the get_db fun (open + create session for db manipulation)
db_dependency = Annotated[Session, Depends(get_db)]

# Pydantic Request Model Validation (for inserting a new Todo)
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# Todos API Endpoints:

# Get all Todos:
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


# Get Todo by ID:
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


# Add Todo (POST):
@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):

    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


# Update Todo (PUT):
@app.put("/todo/{todo_id}", status_code=status.HTTP_201_CREATED)
async def update_todo(db: db_dependency, todo_request: TodoRequest ,todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# Delete Todo:
@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todos).filer(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()