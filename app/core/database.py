
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured in .env")


engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


def get_db_session():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


class Base(DeclarativeBase):
    pass
