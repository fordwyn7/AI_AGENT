from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator

from database.config import config
from database.models import Base


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(
            config.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=config.DEBUG
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        print("✅ Tables created successfully!")
    
    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)
        print("✅ Tables dropped!")
    
    def get_session(self) -> SQLAlchemySession:
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[SQLAlchemySession, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def test_connection(self) -> bool:
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ successful!")
            return True
        except Exception as e:
            print(f"❌ connection failed: {e}")
            return False


db_manager = DatabaseManager()


def get_db() -> Generator[SQLAlchemySession, None, None]:
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()