from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database
from fastapi.security import OAuth2PasswordBearer
from ..auth import decode_access_token
from datetime import datetime

router = APIRouter(tags=["Todo"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = decode_access_token(token)
    if not token_data or not token_data.username:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a Todo
@router.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    new_todo = models.Todo(**todo.dict(), owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# Get Todos grouped
@router.get("/todos")
def get_todos(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    all_todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()

    now = datetime.utcnow()
    grouped = {
        "completed": [],
        "to_be_done": [],
        "time_elapsed": []
    }

    for todo in all_todos:
        if todo.is_completed:
            grouped["completed"].append(todo)
        elif todo.time_to_do < now:
            grouped["time_elapsed"].append(todo)
        else:
            grouped["to_be_done"].append(todo)

    return grouped

# Edit Todo
@router.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    for key, value in todo.dict().items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo

# Mark as completed
@router.put("/todos/{todo_id}/complete")
def mark_complete(todo_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.is_completed = True
    db.commit()
    return {"message": "Todo marked as completed"}

# Delete a Todo
@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == current_user.id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
