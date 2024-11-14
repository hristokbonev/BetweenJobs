from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from dotenv import load_dotenv
from data.database import engine
from data.models.user import User

load_dotenv()

app = FastAPI()

from fastapi import FastAPI
from sqlalchemy import create_engine
from contextlib import asynccontextmanager

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):

    engine = create_engine(DATABASE_URL, echo=True)
    User.metadata.create_all(bind=engine)
    yield
    
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)


# Session management function (using SQLAlchemy session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example route to interact with the database
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI app!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)