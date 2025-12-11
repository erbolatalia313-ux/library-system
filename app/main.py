from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.books.routes import router as books_router
from app.orders.routes import router as orders_router
from app.reports.routes import router as reports_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library System API",
    description="Кітапхана жүйесінің бекенд API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth_router)
app.include_router(books_router)
app.include_router(orders_router)
app.include_router(reports_router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}
