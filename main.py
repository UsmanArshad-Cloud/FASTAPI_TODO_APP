from fastapi import FastAPI, Depends, HTTPException
from pydantic import Field, BaseModel

from Database import SessionLocal, engine
import Models
from sqlalchemy.orm import Session

app = FastAPI()

Models.Base.metadata.create_all(bind=engine)  # Creating Tables


class Todo(BaseModel):
    title: str
    description: str
    priority: int = Field(ge=0, lt=6, description="The Priority must be b/w 0 and 5")
    complete: bool
    owner_id: int


def get_db():  # Creating Database Session
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def ReadAllTodos(db: Session = Depends(get_db)):
    return db.query(Models.Todos).all()


@app.post("/")
async def CreateTodo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = Models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.complete = todo.complete
    todo_model.priority = todo.priority

    db.add(todo_model)
    db.commit()
    return successful_response(201)


@app.put("/")
async def UpdateTodo(todo_id: int
                     , updated_todo: Todo,
                     db: Session = Depends(get_db)):
    todo_model = db.query(Models.Todos).filter(Models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()
    todo_model.title = updated_todo.title
    todo_model.description = updated_todo.description
    todo_model.complete = updated_todo.complete
    todo_model.priority = updated_todo.priority

    db.add(todo_model)
    db.commit()
    return successful_response(200)


@app.delete("/")
async def DeleteTodo(todo_id: int, db: Session = Depends(get_db)):
    if db.query(Models.Todos) \
            .filter(Models.Todos.id == todo_id).first() is not None:
        db.query(Models.Todos).filter(Models.Todos.id == todo_id).delete()
        db.commit()
        return successful_response(200)
    else:
        raise http_exception()


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
