from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import OrderRead
from app.deps import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


# ------------------ Кітапты алу (loan) ------------------ #
@router.post("/loan/{book_id}", response_model=OrderRead)
def loan_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Кітап бар ма?
    book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if not book:
        raise HTTPException(404, detail="Book not found")

    # Бұл кітап қазір біреуде ме?
    active = (
        db.query(models.Order)
        .filter(
            models.Order.book_id == book_id,
            models.Order.return_date.is_(None)
        )
        .first()
    )
    if active:
        raise HTTPException(400, detail="Book already loaned")

    order = models.Order(
        user_id=current_user.user_id,
        book_id=book_id,
        order_date=date.today(),
        return_date=None
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


# ------------------ Кітапты қайтару (return) ------------------ #
@router.post("/return/{order_id}", response_model=OrderRead)
def return_book(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    order = (
        db.query(models.Order)
        .filter(
            models.Order.order_id == order_id,
            models.Order.user_id == current_user.user_id
        )
        .first()
    )

    if not order:
        raise HTTPException(404, detail="Order not found")

    if order.return_date is not None:
        raise HTTPException(400, detail="Book already returned")

    order.return_date = date.today()
    db.commit()
    db.refresh(order)

    return order


# ------------------ Менің барлық тапсырыстарым ------------------ #
@router.get("/my", response_model=List[OrderRead])
def my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    orders = db.query(models.Order).filter(models.Order.user_id == current_user.user_id).all()
    return orders


# ------------------ Қолымдағы белсенді кітаптар ------------------ #
@router.get("/active", response_model=List[OrderRead])
def my_active_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    active_orders = (
        db.query(models.Order)
        .filter(
            models.Order.user_id == current_user.user_id,
            models.Order.return_date.is_(None)
        )
        .all()
    )
    return active_orders
