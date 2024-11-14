from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from config import DATABASE_URL

# Database engine setup
engine = create_engine(DATABASE_URL, echo=True)

# Session setup
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create all tables
def create_db():
    SQLModel.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_session():
    with Session() as session:
        yield session

# Optional: Function to dispose engine after use
def start_db():
    SQLModel.metadata.create_all(bind=engine)
    yield
    engine.dispose()

# Alternative method to get DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
