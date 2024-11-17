from fastapi import FastAPI
from contextlib import asynccontextmanager
from companies.company_router import companies_router
from users.user_router import users_router
from jobposts.jobpost_router import job_post_router
from data.database import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(companies_router)
app.include_router(job_post_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)