from app.database import SessionLocal, Base, engine
from app import models
from app.auth.service import hash_password

# Барлық таблицаларды жасау
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# -------- Admin қолданушы -------- #
admin = models.User(
    name="Admin",
    email="admin@example.com",
    password=hash_password("admin123"),
    role="admin"
)
db.add(admin)


# -------- Қарапайым user -------- #
user = models.User(
    name="User",
    email="user@example.com",
    password=hash_password("user123"),
    role="user"
)
db.add(user)

db.commit()

# -------- Авторлар -------- #
author1 = models.Author(name="Author One")
author2 = models.Author(name="Author Two")

db.add_all([author1, author2])
db.commit()

db.refresh(author1)
db.refresh(author2)

# -------- Кітаптар -------- #
book1 = models.Book(
    title="Book One",
    genre="Novel",
    language="EN",
    author_id=author1.author_id
)

book2 = models.Book(
    title="Book Two",
    genre="Sci-Fi",
    language="RU",
    author_id=author2.author_id
)

db.add_all([book1, book2])
db.commit()

print("✓ Seed data inserted successfully!")
