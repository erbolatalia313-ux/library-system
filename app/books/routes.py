from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import BookRead, BookCreate, BookUpdate
from app.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/books", tags=["Books"])


# ------------------ Кітаптарды алу ------------------ #
@router.get("/", response_model=List[BookRead])
def list_books(
    title: Optional[str] = Query(None),
    genre: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.join(models.Author).filter(models.Author.name.ilike(f"%{author}%"))

    return query.all()


# ------------------ Кітап қосу (ADMIN) ------------------ #
@router.post("/", response_model=BookRead)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # Автор бар ма?
    author = db.query(models.Author).filter(models.Author.author_id == book_in.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_book = models.Book(**book_in.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# ------------------ Кітапты өзгерту (ADMIN) ------------------ #
@router.put("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    book = db.query(models.Book).filter(models.Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in book_in.dict(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


# ------------------ Кітапты өшіру (ADMIN) ------------------ #
@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    book = db.query(models.Book).filter(models.Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}
