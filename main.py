from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from data.database import create_db
import uvicorn
# from routers.api.users_router import router as users_router
from users.user_router import router as user_router
from resumes.resume_routers import router as resumes_router
from users.authentication import users_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(resumes_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)



