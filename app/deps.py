from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.auth.service import decode_access_token

# Login URL — бізде: /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="ыauth/login")


# ------------------- Ағымдағы қолданушы ------------------- #

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:

    token_data = decode_access_token(token)

    if not token_data or not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = db.query(models.User).filter(models.User.user_id == token_data.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ------------------- Тек әкімшілерге рұқсат ------------------- #

def get_current_admin(current_user: models.User = Depends(get_current_user)) -> models.User:

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin has access"
        )

    return current_user
