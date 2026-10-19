
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_CREDENTIALS")

if DATABASE_URL is None:
    raise RuntimeError(f"{DATABASE_URL} is not configured")


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
