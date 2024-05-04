from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import settings

sync_engine = create_engine(settings.SYNC_URL, echo=settings.ECHO)

SessionLocal = sessionmaker(autocommit=settings.AUTOCOMMIT, autoflush=settings.AUTOFLUSH, bind=sync_engine)