from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
 
 
engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session() as session:
        yield session

def start_db():
    SQLModel.metadata.create_all(engine)
    yield
    engine.dispose()

