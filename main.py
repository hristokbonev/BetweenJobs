from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
import csv
from data.database import engine
from sqlmodel import Session
from data.models.user import Users
from confic import DATABASE_URL

 

def configure():
    load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    users = [
        Users(id=1, name="John Doe", first_name="John", last_name="Doe", is_admin=True, date_of_birth="01/01/2000"),
        Users(id=2, name="John Doe1", first_name="John", last_name="Doe1", is_admin=False, date_of_birth="01/11/2000"),
        Users(id=3, name="John Doe2", first_name="John", last_name="Doe2", is_admin=False, date_of_birth="11/01/2000"),   
    ]    

    with Session(engine) as session:
        for user in users:
            db_user = session.get(Users, user.id)
            if db_user is not None:
                continue
            session.add(user)
        session.commit()
    yield


app = FastAPI(lifespan= lifespan)

