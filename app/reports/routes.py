from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models
from app.schemas import PopularBook, TopUser
from app.deps import get_current_admin

router = APIRouter(prefix="/report", tags=["Reports"])


# ------------------ Ең көп алынған кітаптар ------------------ #
@router.get("/most-popular-books", response_model=List[PopularBook])
def most_popular_books(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    rows = (
        db.query(
            models.Book.book_id,
            models.Book.title,
            func.count(models.Order.order_id).label("loan_count")
        )
        .join(models.Order, models.Book.book_id == models.Order.book_id)
        .group_by(models.Book.book_id, models.Book.title)
        .order_by(func.count(models.Order.order_id).desc())
        .limit(10)
        .all()
    )

    return [
        PopularBook(book_id=row[0], title=row[1], loan_count=row[2])
        for row in rows
    ]


# ------------------ Ең белсенді қолданушылар ------------------ #
@router.get("/top-users", response_model=List[TopUser])
def top_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    rows = (
        db.query(
            models.User.user_id,
            models.User.name,
            func.count(models.Order.order_id).label("loan_count")
        )
        .join(models.Order, models.User.user_id == models.Order.user_id)
        .group_by(models.User.user_id, models.User.name)
        .order_by(func.count(models.Order.order_id).desc())
        .limit(10)
        .all()
    )

    return [
        TopUser(user_id=row[0], name=row[1], loan_count=row[2])
        for row in rows
    ]
