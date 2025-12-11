from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr




class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    user_id: int
    role: str

    class Config:
        from_attributes = True




class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None




class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(BaseModel):
    author_id: int
    name: str

    class Config:
        orm_mode = True





class BookBase(BaseModel):
    title: str
    genre: Optional[str] = None
    language: Optional[str] = None
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    author_id: Optional[int] = None


class BookRead(BaseModel):
    book_id: int
    title: str
    genre: Optional[str]
    language: Optional[str]
    author: Optional[AuthorRead]

    class Config:
        orm_mode = True




class OrderRead(BaseModel):
    order_id: int
    user_id: int
    book_id: int
    order_date: date
    return_date: Optional[date] = None

    class Config:
        from_attributes = True




class PopularBook(BaseModel):
    book_id: int
    title: str
    loan_count: int


class TopUser(BaseModel):
    user_id: int
    name: str
    loan_count: int
