from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")

    orders = relationship("Order", back_populates="user")


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50))
    language = Column(String(50))
    author_id = Column(Integer, ForeignKey("authors.author_id"))

    author = relationship("Author", back_populates="books")
    orders = relationship("Order", back_populates="book")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    order_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="orders")
    book = relationship("Book", back_populates="orders")
