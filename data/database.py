from sqlmodel import SQLModel, Session, create_engine
from data.config import DATABASE_URL

# Database engine setup
engine = create_engine(DATABASE_URL, echo=True, connect_args={"connect_timeout": 20})

# Function to create all tables
def create_db():
    SQLModel.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_session():
    with Session(engine) as session:
        yield session
        

# # Optional: Function to dispose engine after use
# def start_db():
#     SQLModel.metadata.create_all(bind=engine)
#     yield
#     engine.dispose()

# def get_db():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()
