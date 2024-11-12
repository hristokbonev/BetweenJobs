from sqlmodel import SQLModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from confic import DATABASE_URL
 
 
SQLModel = declarative_base()
 
engine = create_engine(DATABASE_URL, echo=True)

def create_database():
    SQLModel.metadata.create_all(bind=engine)

 
session_local = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
 
# import your sql alchemy models here
 
 
# def get_db():
#     db = session_local()
#     try:
#         yield db
#     finally:
#         db.close()
 
 
# def create_uuid_extension():
#     with engine.connect() as connection:
#         with connection.begin():
#             connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))