from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional
import models
from models import Books, Users
from database import SessionLocal, engine
from fastapi.responses import JSONResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/books/all')
def get_all_books(user : user_dependency, db = db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    books = db.query(Books).all()
    return books


@app.get('/book/{book_id}')
def get_all_books(user : user_dependency, db : db_dependency, book_id: int):

    if user is None:
        raise HTTPException(status_code=401, detail='Failed Authentication')
    
    book = db.query(Books).filter(Books.id == book_id).first()
    return book