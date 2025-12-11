from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import UserCreate, UserRead, Token
from app.auth.service import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


# ------------------ Register ------------------ #

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):

    # Email бұрын тіркелген бе?
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(400, detail="Email already registered")

    new_user = models.User(
        name=user_in.name,
        email=user_in.email,
        password=hash_password(user_in.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ------------------ Login ------------------ #

from app.schemas import LoginSchema

@router.post("/login", response_model=Token)
def login(credentials: LoginSchema, db: Session = Depends(get_db)):


    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token({
        "user_id": user.user_id,
        "email": user.email,
        "role": user.role
    })

    return Token(access_token=token)
